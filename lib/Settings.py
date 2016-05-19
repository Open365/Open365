import configparser
import random
import os


class Settings:
    def __init__(self,
                 override_settings_path='settings.cfg'):
        self.settingsFilePath = override_settings_path
        self.parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.settings = None
        self.getSettings()

    def getSettings(self):
        self.parser.read('./settings.cfg')
        self.settings = {section: dict(**self.parser[section]) for section in self.parser.sections()}

        return self.settings

    def getServiceIp(self, service):
        return self.settings['general']['my_ip']

if __name__ == '__main__':
    a = Settings()
    for i in range(1, 100):
        print(a.getServiceIp('mongo'))
