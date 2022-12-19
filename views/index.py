"""
Hirespy index (main) view.

URLs include:
/
"""
import os
import logging
import json
import flask
import hirespy
from hirespy.serv.manager import ServerManager
from hirespy.serv.database import get_db

# Log
LOGGER = logging.getLogger(__name__)
LOGGER.debug("Hirespy running...")

# conn = hirespy.model.get_db()
MANAGER = ServerManager()

DB_LOCK = hirespy.app.config['DB_LOCK']
OFFSET = hirespy.app.config['OFFSET']
CAPACITY = hirespy.app.config['CAPACITY']


@hirespy.app.route('/download/<path:filename>')
def download_file(filename):
    """Download upload files."""
    # Check login
    #if "username" not in flask.session:
    #    flask.abort(403)
    hic_path = '/nfs/turbo/umms-drjieliu/usr/temp_Fan/temp_strata/hic'
    # Check file existence
    path = os.path.join(hic_path, filename)[:-1]
    print(path)
    if not os.path.exists(path):
        flask.abort(404)
    return flask.send_from_directory(hic_path,
                                     filename, as_attachment=True)

@hirespy.app.route('/download-200/<path:filename>')
def download_file_200(filename):
    """Download upload files."""
    # Check login
    #if "username" not in flask.session:
    #    flask.abort(403)
    hic_path = '/nfs/turbo/umms-drjieliu/usr/temp_Fan/temp_strata/_pairs'
    # Check file existence
    path = os.path.join(hic_path, filename)[:-1]
    print(path)
    if not os.path.exists(path):
        flask.abort(404)
    return flask.send_from_directory(hic_path,
                                     filename, as_attachment=True)


@hirespy.app.route('/post/<title>/', methods=['GET'])
def show_post(title):
    """Display post."""
    if title not in ["download-tissues-200", "download-tissues", "visit-stat"]:
        flask.abort(404)
    # Query database
    return flask.render_template("{}.html".format(title))


@hirespy.app.route('/', methods=['GET'])
def show_login():
    """Display login."""
    # Check login
    #if "username" in flask.session:
    #    return flask.redirect(flask.url_for('show_index'))

    #if flask.request.method == 'POST':
    #    username = flask.request.form.get("username")
    #    password = flask.request.form.get("password")
    #    if not insta485.model.validate(username, password):
    #        flask.abort(403)
    #    flask.session['username'] = username
    #    return flask.redirect(flask.url_for('show_index'))

    # Query database
    return flask.render_template("login.html")



@hirespy.app.route('/caesar/', methods=['GET', 'POST'])
def index():
    """Display / route."""
    #if "username" not in flask.session:
    #    return flask.redirect(flask.url_for('show_login'))
    # Add database info to context
    context = {
        "datasets": [],
        # "region": "",
        # "entered": False,
        # "result": "Details will be shown here...",
        # "userid": "",
        # "port": "",
    }
    conn = get_db()
    DB_LOCK.acquire()
    context["datasets"] = conn.execute(
        "SELECT id, name, path "
        "FROM datasets ",
    ).fetchall()
    DB_LOCK.release()

    return flask.render_template("index.html", **context)

@hirespy.app.route('/progress/<pid>')
def progress(pid):
    """Progress bar response."""
    # def generate():
    #    x = 0
    #    while x <= 100:
    #        yield "data:" + str(x) + "\n\n"
    #        x = x + 1
    #        time.sleep(0.5)
    def query():
        conn = get_db()
        LOGGER.debug("Respond to %s", str(pid))
        DB_LOCK.acquire()
        data = conn.execute(
            "SELECT progress, port, msg "
            "FROM requests "
            "WHERE id = ?",
            (int(pid),)).fetchone()
        conn.commit()
        DB_LOCK.release()
        if data is not None:
            prog = data["progress"]
            port = data["port"]
            msg = data["msg"]
        else:
            prog = 99
            port = 3000
            msg = "An error occurred.\nPlease Try again."
        temp = {
            "prog": str(prog),
            "result": "https://nucleome.dcmb.med.umich.edu/port/{}".format(port) +
                      "\nIdentification: {} (Please check whether this id matches)".format(pid),
            "msg": msg
        }
        json_obj = json.dumps(temp)
        if prog == 100:
            LOGGER.warning("Send Message: %s", json_obj)
        return "retry: 3000\ndata:" + json_obj + "\n\n"
    # print(query())
    return flask.Response(query(), mimetype='text/event-stream')

"""
    # POST handler
    if flask.request.method == 'POST':
        if flask.request.content_length > 1024:
            flask.abort(413)
            return 1
        region = flask.request.form.get("region")
        d_type = flask.request.form.get("type")
        if not region:
            context["region"] = "Cannot be empty"
            return flask.render_template("index.html", **context)
        LOGGER.warning("Receiving type data: %s %s", d_type, region)
        nport, nid = MANAGER.add(region)
        context["region"] = region
        context["entered"] = True
        context["userid"] = str(nid)
        context["port"] = str(nport)
"""
