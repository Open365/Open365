from lib.Settings import Settings
import requests
from lib.Wrappers.Logger import Logger
from lib.Errors.EyeosAPIError import EyeosAPIError
from lib.EyeosApi.EyeosApiCall import EyeosApiCall


class Application:
    def __init__(self, injected_proxy_ip=None,
                 injected_api_call=None):
        self.proxy_ip = injected_proxy_ip or Settings().getServiceIp('proxy')
        self.api_call = injected_api_call or EyeosApiCall()
        self.logger = Logger(__name__)

    def insert_apps(self, apps, card):
        apps_url = "https://{0}/application/v1/applications".format(self.proxy_ip)
        self.logger.debug('POST request to: {0}'.format(apps_url))
        req = self.api_call.post(apps_url, card=card, verify=False, json=apps)

        if req.status_code != 201:
            raise EyeosAPIError("Error inserting apps. API response: [ code: {0}, content: {1}]"
                                .format(req.status_code, req.content))

        self.logger.info('Apps correctly installed.')

    def empty_apps(self, card):
        apps_url = "https://{0}/application/v1/applications".format(self.proxy_ip)
        self.logger.debug('DELETE request to: {0}'.format(apps_url))
        req = self.api_call.delete(apps_url, card=card, verify=False)

        if req.status_code != 200:
            raise EyeosAPIError("Error emptying apps. API response: [ code: {0}, content: {1}]"
                                .format(req.status_code, req.content))

        self.logger.info('Apps correctly emptied.')

    def save(self, apps, card):
        self.insert_apps(apps['eyeosApps'], card)
