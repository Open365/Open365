from lib.Settings import Settings
from pymongo import MongoClient


class EyeosAppsStorage:

    def __init__(self, injected_applications=None):
        self.controlpanel_applications = injected_applications or MongoClient(
            Settings().getServiceIp('mongo')
        ).eyeos.controlpanelapplications

    def save(self, apps):

        self.controlpanel_applications.delete_many({})
        self.controlpanel_applications.insert_many(apps['controlPanelApps'])
