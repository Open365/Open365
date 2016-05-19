import os
import shutil
import subprocess

from lib.Settings import Settings
from lib.Tools import paths
from lib.Wrappers.Logger import Logger


class FileSystem:

    def __init__(self, injectedSettings=None, injectedSubprocess=None):
        self.logger = Logger(__name__)
        self.settings = injectedSettings or Settings().getSettings()
        self.subprocess = injectedSubprocess or subprocess

    def clean_filesystem(self):
        self.logger.info("Cleaning filesystem.")
        self._clean_files(paths.raw_fs)
        self.logger.info("Cleaning databases.")
        self._clean_files(paths.data + "/db")
        self.logger.info("Cleaning LDAP.")
        self._clean_files(paths.data + "/ldap")
        self.logger.info("Cleaning elasticsearch.")
        self._clean_files(paths.data + "/elasticsearch")
        self.logger.info("Cleaning MySql.")
        self._clean_files(paths.data + "/mysql")
        self.logger.info("Cleaning Seafile Sync Files.")
        self._clean_files(paths.data + "/seafilesync")
        self.logger.info("Cleaning Seafile Raw Data.")
        self._clean_files(paths.data + "/seafileRawData")

    def _clean_files(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            if not os.path.exists(path):
                os.makedirs(path)

    def create_skel(self, username, domain):
        self.logger.debug("Creating folders for " + username)
        list_of_dirs = ["config", "files", "local", "mailbox", "networkdrives", "workgroups"]
        if self.settings['general']['multitenant'] == "true":
            base_path = paths.raw_fs + "/users/" + domain + "/" + username + "/"
        else:
            base_path = paths.raw_fs + "/users/" + username + "/"
        mode = 0o755
        for directory in list_of_dirs:
            os.makedirs(base_path + directory, mode, exist_ok=True)
            self.logger.debug("Created " + base_path + directory)
        os.system("chmod 777 " + base_path + "mailbox")
