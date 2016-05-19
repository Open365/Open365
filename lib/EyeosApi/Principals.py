import json
import requests

from lib.EyeosApi.EyeosApiCall import EyeosApiCall
from lib.Settings import Settings
from lib.Wrappers.Logger import Logger


class Principals:
    def __init__(self, proxy_ip=None, injected_eyeos_api_call=None):
        self.proxy_ip = proxy_ip or Settings().getServiceIp('proxy')
        self.systemgroups_url = 'https://{0}/systemgroups/v1/systemgroups'.format(self.proxy_ip)
        self.logger = Logger(__name__)
        self.eyeos_api_call = injected_eyeos_api_call or EyeosApiCall()

    def get_systemgroup(self, group_id, eyeos_card):
        response = self.eyeos_api_call.get(self.systemgroups_url + '/' + group_id, verify=False, card=eyeos_card)
        return response.json()

    def put_systemgroup(self, group, eyeos_card):
        response = self.eyeos_api_call.put(self.systemgroups_url + '/' + group['_id'],
                                           verify=False,
                                           card=eyeos_card,
                                           headers={"Content-Type": "application/json"},
                                           json=group)
        return response.json()
