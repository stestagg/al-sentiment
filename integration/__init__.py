import os
import inspect
import sys
import subprocess
import socket
import time


ROOT = os.path.dirname(os.path.dirname(
    inspect.getfile(inspect.currentframe())))


# Copied from trms code, slightly less-ugly way to wait for server to become
# available

def is_child_running(pid):
    """Tests if a process is still alive"""
    try:
        res = os.waitpid(pid, os.WNOHANG)
    except OSError:
        return False
    return res == (0, 0)


def wait_port(pid, port, host="127.0.0.1", timeout=5):
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(timeout)
    start = time.time()
    while True:
        try:
            if not is_child_running(pid):
                raise AssertionError(
                    "Waiting for port from process that isn't running")
            sock.connect((host, port))
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except socket.error:
            pass
        else:
            return
        if timeout <= (time.time() - start):
            raise AssertionError(
                "Timeout waiting for port to become available")
        time.sleep(0.1)


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
        cls.PROC = subprocess.Popen([
            sys.executable,
            os.path.join(ROOT, "sentiment", "server.py"),
            "--port=%s" % (cls.PORT)])
        # This is *ugly* but quick and simple for now,
        # TODO: use socket polling with process monitoring
        try:
            wait_port(cls.PROC.pid, cls.PORT)
        except:
            cls.PROC.terminate()
            raise

    @classmethod
    def stop(cls):
        if cls.PROC:
            cls.PROC.terminate()
        cls.PROC = None


def setUpModule():
    Webserver.start()


def tearDownModule():
    Webserver.stop()
