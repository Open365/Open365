import time

from lib.DomainObjects.EyeosCard import EyeosCard
from lib.Errors.EyeosAPIError import EyeosAPIError
from lib.EyeosApi.EyeosApiCall import EyeosApiCall
from lib.Settings import Settings
from lib.Wrappers.Logger import Logger


class Logout:

    def __init__(self, injected_proxy_ip=None, injected_eyeos_api_call=None):
        self.settings = Settings().getSettings()
        self.proxy_ip = injected_proxy_ip or self.settings['general']['public_hostname']
        self.logger = Logger(__name__)
        self.eyeos_api_call = injected_eyeos_api_call or EyeosApiCall()

    def logout(self, card):
        self.logger.info("Retrieving a valid card...")
        data = {
            'timestamp': int(time.time())
        }

        logout_url = "https://{0}/relay/presence/v1/routingKey/logout/userEvent/logout".format(self.proxy_ip)
        self.logger.debug('POST request to: {0}'.format(logout_url))
        req = self.eyeos_api_call.post(logout_url, verify=False, data=data, card=card)
        if req.status_code != 200:
            raise ValueError("Error logging out with user")
