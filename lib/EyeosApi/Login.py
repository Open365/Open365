import getpass

from lib.DomainObjects.EyeosCard import EyeosCard
from lib.Errors.EyeosAPIError import EyeosAPIError
from lib.EyeosApi.EyeosApiCall import EyeosApiCall
from lib.Settings import Settings
from lib.Wrappers.Logger import Logger


class Login:

    def __init__(self, injected_proxy_ip=None, injected_eyeos_api_call=None):
        self.settings = Settings().getSettings()
        self.proxy_ip = injected_proxy_ip or self.settings['general']['public_hostname']
        self.logger = Logger(__name__)
        self.eyeos_api_call = injected_eyeos_api_call or EyeosApiCall()

    def authenticate(self, username, password, domain=False):
        if not domain:
            domain = self.settings['general']['default_domain']
        self.logger.info("Retrieving a valid card...")
        data = {
            'type': 'Basic',
            'username': username,
            'password': password,
            'domain': domain
        }

        auth_url = "https://{0}/login/v1/methods/login/".format(self.proxy_ip)
        self.logger.debug('POST request to: {0}'.format(auth_url))
        req = self.eyeos_api_call.post(auth_url, verify=False, json=data)

        if req.status_code != 200:
            raise ValueError("Error authenticating with user {0} (Check if captcha is preventing access)"
                             .format(data['username']))

        try:
            login_card = req.json()
        except ValueError as e:
            raise EyeosAPIError("Error parsing JSON response: {0}".format(req.content)) from e

        try:
            return EyeosCard(login_card['card'], login_card['signature'])
        except KeyError as e:
            raise EyeosAPIError("Can't retrieve card form login API") from e
