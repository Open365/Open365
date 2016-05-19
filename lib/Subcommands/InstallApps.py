import getpass

from lib.Wrappers.ArgumentParser import ArgumentParser
from lib.EyeosApps.EyeosApps import EyeosApps
from lib.Settings import Settings


class InstallApps:
    def __init__(self, eyeos_apps=None):
        self.eyeos_apps = eyeos_apps or EyeosApps()
        self.settings = Settings().getSettings()
        self.admin_username = self.settings['general']['administrator_username']
        self.admin_domain = self.settings['general']['default_domain']

    def execute(self, *args):
        args = self._parse_arguments(*args)
        try:
            password = args.password
            if password is None:
                password = getpass.getpass("Enter '{0}' password:".format(args.user))
            if password is '':
                raise ValueError("Invalid password")
            self.eyeos_apps.install(args.appsDirectory, args.user, password, self.admin_domain)
        except (ValueError, FileNotFoundError) as e:
            exit(e)

    def _parse_arguments(self, command_name, *args):
        parser = ArgumentParser(description='Install eyeos apps',
                                prog='eyeos ' + command_name)
        parser.add_argument('appsDirectory', metavar='APPS_DIRECTORY', nargs='?', default=EyeosApps.DEFAULT_APPS_DIR,
                            help='directory with the eyeos apps to install')
        parser.add_argument('--user', metavar='USERNAME', default=self.admin_username,
                            help='Administrator user')
        parser.add_argument('--password', metavar='PASSWORD', default=None,
                            help='Administrator password')

        args = parser.parse_args(args)
        return args
