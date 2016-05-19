import subprocess as global_subprocess
from lib.Wrappers.Logger import Logger


class LocalPortCheck:
    def __init__(self, subprocess=None):
        self.logger = Logger(__name__)
        self.subprocess = subprocess or global_subprocess

    def is_opened(self, port):
        exitcode = self.subprocess.call('netstat -lntp | grep -q ":' + str(port) + ' "', shell=True)
        if exitcode == 0:
            return True
        return False
