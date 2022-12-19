"""Server."""
import os
import logging
import subprocess
import threading
import shlex
import signal
from enum import Enum
import hirespy
from hirespy.serv.database import get_db


DB_LOCK = hirespy.app.config['DB_LOCK']


class Status(Enum):
    """Server status enum."""

    STOPPED = 0
    STARTING = 1
    RUNNING = 2
    STOPPING = 3


class Server():
    """Define class for server."""

    prefix = "config_"

    # status 0 stopped 1 running 2 stopping 3 stopped

    def __init__(self, port):
        """Initialize the server object."""
        super(Server, self).__init__()
        self.port = str(port)
        self.sheet = self.__sheet()
        self.status = Status.STOPPED
        self.logger = logging.getLogger("server.{}".format(self.port))
        self.logger.debug("Server Initialized. (port:%s)", str(self.port))
        self.process = None

    def __sheet(self):
        """Generate sheet name."""
        return "{}{}.xlsx".format(Server.prefix, self.port)

    def start(self, flag=True):
        """Start the server."""
        cmd = shlex.split(os.path.join(hirespy.app.config['FILE_FOLDER'],
                                       "nucleserver") +
                          " start -i " +
                          os.path.join(hirespy.app.config['SHEET_FOLDER'],
                                       self.sheet) +
                          " -p " +
                          self.port)
        # print(cmd)
        self.logger.info("Starting server... (port:%s)", str(self.port))
        self.status = Status.STARTING  # starting
        self.process = subprocess.Popen(cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        # Starting
        while self.process.poll() is None:
            line = self.process.stdout.readline()
            #while line:
            #    print(line)
            #    line = self.process.stdout.readline()
            #print([i.strip().decode('utf-8') for i in self.process.stdout.readlines()])
            line = line.strip().decode('utf-8')
            if line:
                # print(line)
                self.logger.info("Server is running... (port:%s)",
                                 str(self.port))
                self.status = Status.RUNNING  # running
                break
        # Fail
        if self.process.poll() is not None:
            self.logger.error("Failed to start server (port:%s)",
                              str(self.port))
            self.status = Status.STOPPED
        # Finish
        prog = 100
        msg = "Finished."
        if not flag:
            prog = 99
            msg = "Failed. Please check input."
        with hirespy.app.app_context():
            conn = get_db()
            DB_LOCK.acquire()
            conn.execute(
                "UPDATE requests "
                "SET progress = ?, msg = ? "
                "WHERE port = ?",
                (prog, msg, self.port,)
            )
            conn.commit()
            DB_LOCK.release()
        return True

    def stop(self):
        """Stop the server."""
        # Stopped
        if self.status == Status.STOPPED:
            self.logger.warning("Server was stopped. (port:%s)",
                                str(self.port))
            return True
        # Stopping
        if self.status == Status.STOPPING:
            self.logger.warning("Server is being stopped. (port:%s)",
                                str(self.port))
            return False
        # Starting
        while self.status == Status.STARTING:
            pass
        # Running
        if self.status == Status.RUNNING:
            self.status = Status.STOPPING
            self.process.send_signal(signal.SIGINT)
            self.logger.debug("Stop signal sent to server. (port:%s)",
                              str(self.port))
            while self.process.poll() is None:
                pass
            self.logger.info("Server is stopped. (port:%s)", str(self.port))
            self.status = Status.STOPPED
        return True

    def restart(self):
        """Restart the server."""
        while not self.stop():
            self.stop()
        self.start()
