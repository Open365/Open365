import time

import requests
from lib.Settings import Settings
from lib.Errors.UnknownHostError import UnknownHostError
from lib.Wrappers.Logger import Logger

import logging


class WaitForEyeos:
    def __init__(self):
        self.settings = Settings()
        self.logger = Logger(__name__)
        self.entrypoint = "proxy"

    def wait(self, timeout):
        logging.getLogger("requests").setLevel(logging.ERROR)
        starttime = time.time()
        while True:
            now = time.time()
            if now - starttime > timeout:
                raise TimeoutError("Wait timed out")
            try:
                ip = self.settings.getServiceIp(self.entrypoint)
                requests.get('http://{0}'.format(ip), verify=False)
                time.sleep(5)
                self.logger.info("Waited for {0} seconds".format(int(now - starttime)))
                break
            except (UnknownHostError, requests.exceptions.RequestException) as e:
                time.sleep(0.5)
                continue
