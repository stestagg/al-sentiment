import os
import inspect
import sys
import subprocess
import socket
import time


ROOT = os.path.dirname(os.path.dirname(
    inspect.getfile(inspect.currentframe())))


class Webserver(object):

    """
    Represents a running test webserver, Webserver.BASE_URL can be used
    to make HTTP requests against the server
    """

    # This should be dynamically generated, but for now I will hard-code a port
    PORT = 5542
    BASE_URL = "http://127.0.0.1:%s/" % (PORT, )
    PROC = None

    @classmethod
    def start(cls):
        cls.PROC = subprocess.Popen([os.path.join(ROOT, "runserver"),
                                     "--port=%s" % (cls.PORT)])
        # This is *ugly* but quick and simple for now,
        # TODO: use socket polling with process monitoring
        time.sleep(1)

    @classmethod
    def stop(cls):
        if cls.PROC:
            cls.PROC.terminate()
        cls.PROC = None


def setUpModule():
    Webserver.start()


def tearDownModule():
    Webserver.stop()
