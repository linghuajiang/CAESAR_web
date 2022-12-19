"""Server manager."""

import os
import shutil
import logging
import threading
import openpyxl
import jinja2
from pathlib import Path
import hirespy
from time import sleep
from hirespy.serv.server import Server
from hirespy.serv.database import get_db
from hirespy.attr.attribution import attribution
from hirespy.attr.utils import model_fn, parse_coordinate

DB_LOCK = hirespy.app.config['DB_LOCK']
APP_LOCK = hirespy.app.config['LOCK']
logger = logging.getLogger(__name__)
signals = ['ATAC_seq', 'CTCF', 'H3K4me1', 'H3K4me3',
           'H3K9ac', 'H3K27ac', 'H3K27me3', 'H3K36me3']
signals = ['ATAC_seq', 'CTCF', 'H3K4me1', 'H3K4me3', 'H3K27ac', 'H3K27me3']

class ServerManager():
    """ServerManage class."""

    def __init__(self):
        """Initialize the manager object."""
        super(ServerManager, self).__init__()
        self.cap = hirespy.app.config['CAPACITY']  # capacity, number of maximum clients
        self.offset = hirespy.app.config['OFFSET']  # port offset, starting port number
        self.total = 0  # id count, total number of requests
        self.server = []  # nucleserver list
        self.threads = []  # thread list
        self.id = []  # id list

        # initial database
        self.init_db()

        # init server and thread (plus one for main set)
        self.init_hic()
        self.init_eqtl()
        self.init_as()
        for i in range(self.cap + 1):
            self.id.append(i)
            self.server.append(Server(self.offset + i))
            self.threads.append(None)
        
        # start thread
        #init_input = None
        #for i in range(self.cap + 1):
        #    self.start(i, init_input)

    def init_db(self):
        """Insert database values."""
        # Initialize database entries
        with hirespy.app.app_context():
            conn = get_db()
            for i in range(self.cap + 1):
                DB_LOCK.acquire()
                conn.execute(
                    "INSERT INTO requests(id, port, progress, msg, data) "
                    "VALUES (?, ?, 0, 'Initialized', 'None')",
                    (i, (self.offset + i),)
                )
                conn.commit()
                DB_LOCK.release()

    def init_hic(self):
        """Initialize nucleservers serving hic files."""
        hic_offset = hirespy.app.config['HIC_OFFSET']  # port offset, starting port number
        hic_list = []
        with hirespy.app.app_context():
            conn = get_db()
            hic_list = conn.execute(
                "SELECT * "
                "FROM datasets "
            ).fetchall()
        for hic in hic_list:
            req = {
                'tissue': '_'.join(hic['name'].split(' ')),
                'tissue_path': os.path.join(hic['path']),
                'code': hic['path'].split('/')[-1][:-4],
                'port': hic_offset + hic['id']
            }
            self.init_xlsx(req)
            self.gen_json_tissue(req)
            Server(req['port']).start()

        # print(hic_list)

    def init_xlsx(self, req):
        """Create excel config files."""
        sheetpath = hirespy.app.config['SHEET_FOLDER']  # /var/www/data/sheets
        datapath = hirespy.app.config['DATA_FOLDER']  # /var/www/data
        tmlpath = os.path.join(hirespy.app.config['TEMPLATE_FOLDER'], 'config_.xlsx')  # config excel sheet template
        port = req['port']  # port number

        # Set filename
        dest = os.path.join(sheetpath, 'config_{}.xlsx'.format(port))
        try:
            os.remove(dest)
        except:
            print("No such file or directory:"+dest)

        # Load Template
        work_book = openpyxl.load_workbook(filename=tmlpath)
        if req.get('tracks_path') is None:
            name = req['tissue']
        else:
            name = "USER-{}".format(req['id'])

        # HiC data folder /nfs/turbo/umms-drjieliu/usr/yyao/hic/
        work_sheet = work_book["Config"]
        # work_sheet["B2"] = "/nfs/turbo/umms-drjieliu/usr/yyao/"
        work_sheet["B2"] = "/nfs/turbo/umms-drjieliu/usr/"
        # 
        work_sheet = work_book["Index"]
        work_sheet["A2"] = "hg38"
        work_sheet["B2"] = name
        work_sheet = work_book["ENCODE"]
        work_sheet.title = name
        work_sheet[f"A2"] = "refSeq_hg38"
        work_sheet[f"B2"] = './lhjiang/nucleome_server/igv_refseq.bb'
        work_sheet[f"A3"] = Path(req['tissue_path']).stem  # "m0"
        work_sheet[f"B3"] = os.path.join('./temp_Fan/temp_strata/hic', req['tissue_path'].split('/')[-1])
        print(req['tissue_path'])
        work_sheet[f"A4"] = ''
        work_sheet[f"B4"] = ''
        cnt = 4
        if req.get('eqtl_path') is not None:
            work_sheet[f"A4"] = "GTEx_cis-eQTLs"
            work_sheet[f"B4"] = './lhjiang/nucleome_server/gtexCaviar.bb'
        if req.get('as_path') is not None:
            #work_sheet[f"A2"] = "GENCODE_v39"
            #work_sheet[f"B2"] = './lhjiang/nucleome_server/gencodeV39.bb'
            for index,value in enumerate(['ATAC_seq','CTCF','H3K4me1', 'H3K4me3', 'H3K27ac', 'H3K27me3']):
                work_sheet[f"A{index+4}"] = value + "_m"
                work_sheet[f"B{index+4}"] = os.path.join('./lhjiang/nucleome_server/data', req['tissue'] + "_m_" + value + ".bigWig")
            for index,value in enumerate(['ATAC_seq','CTCF','H3K4me1', 'H3K4me3', 'H3K27ac', 'H3K27me3']):
                work_sheet[f"A{index+10}"] = value + "_p"
                work_sheet[f"B{index+10}"] = os.path.join('./lhjiang/nucleome_server/data', req['tissue'] + "_p_" + value + ".bigWig")
        if req.get('tracks_path') is not None:  # None if it is a tissue only server
            for _, _, files in os.walk(req['tracks_path']):
                for filename in files:
                    work_sheet[f"A{cnt}"] = str(req['id']) + "_" + Path(filename).stem  # f"t{cnt}"
                    work_sheet[f"B{cnt}"] = os.path.join('./yyao/temp_tracks', str(req['index']), filename)
                    cnt += 1
        work_book.save(filename=dest)
        logger.debug('Config file created. (id:%s)', port)

    def gen_json_tissue(self, req):
        """Generate JSON."""
        temp = hirespy.app.config["TEMPLATE_FOLDER"]
        path = hirespy.app.config["JSON_FOLDER"]
        context = {
            "name" : req['tissue'],
            "code": req['code'],
            "chr": "chr1",
            "start": 53820000,
            "end": 53930000,
            "length": 159345973,
            "port": req['port'],
        }
        json_name = "port{}.json".format(req['port'])
        result = (jinja2.Environment(
            loader=jinja2.FileSystemLoader(temp)
        ).get_template("template_tissue.json").render(context))
        
        with open(os.path.join(path, json_name), "w+") as filename:
            filename.writelines([result])

    def gen_json_eqtl(self, req):
        """Generate JSON."""
        temp = hirespy.app.config["TEMPLATE_FOLDER"]
        path = hirespy.app.config["JSON_FOLDER"]
        context = {
            "name" : req['tissue'],
            "code": req['code'],
            "chr": "chr1",
            "start": 53820000,
            "end": 53930000,
            "length": 159345973,
            "port": req['port'],
        }
        json_name = "port{}.json".format(req['port'])
        result = (jinja2.Environment(
            loader=jinja2.FileSystemLoader(temp)
        ).get_template("template_eqtl.json").render(context))
        
        with open(os.path.join(path, json_name), "w+") as filename:
            filename.writelines([result])

    def gen_json_as(self, req):
        """Generate JSON."""
        temp = hirespy.app.config["TEMPLATE_FOLDER"]
        path = hirespy.app.config["JSON_FOLDER"]
        context = {
            "name" : req['tissue'],
            "code": req['code'],
            "chr": "chr1",
            "start": 53820000,
            "end": 53930000,
            "length": 159345973,
            "port": req['port'],
        }
        json_name = "port{}.json".format(req['port'])
        result = (jinja2.Environment(
            loader=jinja2.FileSystemLoader(temp)
        ).get_template("template_as.json").render(context))
        
        with open(os.path.join(path, json_name), "w+") as filename:
            filename.writelines([result])
    
    def gen_json(self, position, req):
        """Generate JSON."""
        temp = hirespy.app.config["TEMPLATE_FOLDER"]
        path = hirespy.app.config["JSON_FOLDER"]
        context = {
            "chr": "chr7",
            "start": 0,
            "end": 0,
            "chr1" : "chr7",
            "start1": 53820000,
            "end1": 53930000,
            "chr2": "chr7",
            "start2": 53820000,
            "end2": 53930000,
            "user_id": 0,
            "port": 3000,
            "code": "NAME",
        }
        chr_, p11, p12, p21, p22 = position
        context["chr"] = req['bg']['chr']
        context["chr1"] = chr_
        context["chr2"] = chr_
        context["start"] = req['bg']['start']
        context["start1"] = p11
        context["start2"] = p21
        context["end"] = req['bg']['end']
        context["end1"] = p12
        context["end2"] = p22
        context["user_id"] = req['id']
        context["port"] = req['port']
        context["code"] = req['code']
        json_name = "port{}.json".format(req['port'])
        result = (jinja2.Environment(
            loader=jinja2.FileSystemLoader(temp)
        ).get_template("template.json").render(context))##
        
        with open(os.path.join(path, json_name), "w+") as filename:
            filename.writelines([result])

            
        json_name = "port{}i.json".format(req['port'])
        result = (jinja2.Environment(
            loader=jinja2.FileSystemLoader(temp)
        ).get_template("template_interactive.json").render(context))##
        
        with open(os.path.join(path, json_name), "w+") as filename:
            filename.writelines([result])

    def setup_server(self, req):
        """Load data and start nucleserver."""
        index = req['index']
        # Stop the server on the port if any
        self.server[index].stop()
        # log starting
        with hirespy.app.app_context():
            conn = get_db()
            DB_LOCK.acquire()
            conn.execute(
                "UPDATE requests "
                "SET progress = 30, msg = ? "
                "WHERE port = ?",
                ("Processing data...", req['port'],))
            conn.commit()
            DB_LOCK.release()
        logger.info("Starting thread. (port:%s)", req['port'])
        # prepare tracks path
        try:
            if req.get('tracks_path') is not None:
                shutil.rmtree(req['tracks_path'])
        except FileNotFoundError:
            pass
        finally:
            os.mkdir(req['tracks_path'])

        # Attribution
        flag = True  # success or not
        positon = None
        if req.get('tracks_path'):
            try:
                if req['marks'] == '':
                    raise ValueError('Test.')
                positon = attribution(req, signals)
                self.gen_json(positon, req)
            except ValueError as value_error:
                flag = False
                logger.error(value_error)
                logger.error("Wrong input %s", req["region"])

        # log starting server
        with hirespy.app.app_context():
            conn = get_db()
            DB_LOCK.acquire()
            conn.execute(
                "UPDATE requests "
                "SET progress = 80, msg = ? "
                "WHERE port = ?",
                ("Starting server...", str(index + self.offset),))
            conn.commit()
            DB_LOCK.release()

        self.init_xlsx(req)
        self.server[index].start(flag)

    def start(self, index, req):
        """Start a server (Thread wrapper)."""
        # wait for join
        if self.threads[index] and self.threads[index].isAlive():
            self.threads[index].join()
        # create thread
        self.threads[index] = threading.Thread(target=self.setup_server,
                                               args=(index, req))
        self.threads[index].start()

    def stop(self, index):
        """Stop a server."""
        if self.threads[index].isAlive():
            self.threads[index].join()
        logger.debug("Finish thread. (port:%s)", str(self.offset + index))
        self.threads[index] = threading.Thread(target=self.server[index].stop,
                                               args=())
        self.threads[index].start()

    def thread_wrapper(self, index, req):
        """
        Thread wrapper.
        Close the previous nucleserver and open up a new one.
        """
        pass

    def init_eqtl(self):
        eqtl_offset = hirespy.app.config['EQTL_OFFSET']  # port offset, starting port number
        eqtl_list = []
        with hirespy.app.app_context():
            conn = get_db()
            eqtl_list = conn.execute(
                "SELECT * "
                "FROM datasets"
            ).fetchall()
        for donor in eqtl_list:
            req = {
                'tissue': '_'.join(donor['name'].split(' ')),
                'tissue_path': donor['path'],
                'eqtl_path': os.path.join(donor['path']),
                'code': donor['path'].split('/')[-1][:-4],
                'port': eqtl_offset + donor['id']
            }
            self.init_xlsx(req)
            self.gen_json_eqtl(req)
            Server(req['port']).start()

    def init_as(self):
        as_offset = hirespy.app.config['AS_OFFSET']  # port offset, starting port number
        as_list = []
        with hirespy.app.app_context():
            conn = get_db()
            as_list = conn.execute(
                "SELECT * "
                "FROM asdata"
            ).fetchall()
        for donor in as_list:
            req = {
                'tissue': '_'.join(donor['name'].split(' ')),
                'tissue_path': donor['path'],
                'as_path': os.path.join(donor['path']),
                'code': donor['name'],
                'port': as_offset + donor['id']
            }
            self.init_xlsx(req)
            self.gen_json_as(req)
            Server(req['port']).start()


    def add(self, req):
        """
        Add a server.
        red: tissue, region, tissue_path, tracks_path, id, port
        """
        user_id = self.total + 1  # get the new id
        index = (user_id - 1) % self.cap + 1  # calculate index

        # return 0, 0 when the server is busy, which will be handled in html
        if self.threads[index] and self.threads[index].isAlive():
            return 0, 0
        
        self.id[index] = user_id
        port = index + self.offset
        logger.debug("Manager restarts id(%s) port(%s)",
                          str(user_id), str(port))
        DB_LOCK.acquire()
        conn = get_db()
        # log request
        conn.execute(
            "UPDATE requests "
            "SET id = ?, progress = 0, msg = ?, data = ? "
            "WHERE port = ? ",
            (str(user_id), "Request received", req["tissue_id"] + " " + req["region"], str(port),))
        conn.commit()
        # get tissue path
        paths = conn.execute(
            "SELECT name, path, marks "
            "FROM datasets "
            "WHERE id = ?",
            (req["tissue_id"],)
        ).fetchone()
        req["tissue"] = paths["name"]
        subpath = paths["path"]
        marksdir = paths["marks"]
        DB_LOCK.release()

        req['tissue_path'] = paths["path"]
        req['tracks_path'] = \
            os.path.join('/nfs/turbo/umms-drjieliu/usr/yyao/temp_tracks', str(index))
        req['port'] = port
        req['id'] = user_id
        req['index'] = index
        req['code'] = req['tissue_path'].split('/')[-1][:-4]
        req['marks'] = paths["marks"]

        self.total += 1

        self.threads[index] = threading.Thread(target=self.setup_server,
                                               args=(req,))
        self.threads[index].start()

        return port, user_id

    def get_thread(self, index):
        """Return thread."""
        return self.threads[index]
