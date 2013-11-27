import os
import inspect
import sys
import subprocess
import time


ROOT = os.path.dirname(os.path.dirname(
    inspect.getfile(inspect.currentframe())))


class Webserver(object):

    # This should be dynamically generated, but for now I will hard-code a port
    PORT = 5543
    BASE_URL = "http://localhost:%s/" % (PORT, )
    PROC = None

    @classmethod
    def start(cls):
        cls.PROC = subprocess.Popen([
            sys.executable,

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
