import sys
import re

from lib.Wrappers.ArgumentParser import ArgumentParser
from lib.Wrappers.Logger import Logger
from lib.Users.UsersManagement import UsersManagement
from lib.Settings import Settings
from lib.DomainManagement.Domain import Domain


class UserCreate:
    def __init__(self):
        self.logger = Logger(__name__)
        self.userManagement = UsersManagement()
        self.settings = Settings().getSettings()
        self.domain = Domain()

    def execute(self, *args):
        args = self._parse_arguments(*args)
        args.user[0] = args.user[0].lower()
        if self.validateUsername(args.user[0]) is False:
            self.logger.error("The username '" + args.user[0] + "' contains illegal characters.  "
                              "(A username may only contain letters, numbers, underscores, dashes, and dots)")
            sys.exit(1)
        if self.domain.domain_exists(args.domain) is False:
            self.logger.error("The domain " + args.domain + " does not exist. "
                              "Cannot add user to non existing domain \n"
                              "To create this domain execute: sudo eyeos create-domain " + args.domain)
            sys.exit(1)
        if self.userManagement.createUser(args):
            pass
            # sys.exit(0)
        else:
            sys.exit(1)

    def _parse_arguments(self, command_name, *args):
        parser = ArgumentParser(description='Users creation',
                                prog='eyeos ' + command_name)
        parser.add_argument('user', metavar='USERNAME', nargs=1,
                            help='username of the user to delete')
        parser.add_argument('--domain', metavar='DOMAIN', required=False,
                            default=self.settings['general']['default_domain'],
                            help='Insert the domain of the user')
        parser.add_argument('--firstname', metavar='NAME', default=False,
                            help='Insert the firstname when create a user')
        parser.add_argument('--surname', metavar='SURNAME', required=True,
                            help='Insert the surname when create a user')
        parser.add_argument('--password', metavar='PASSWORD', required=True,
                            help='Insert the password when create a user')
        parser.add_argument('--email', metavar='EMAIL', required=True,
                            help='Insert the email when create a user')
        args = parser.parse_args(args)
        return args

    def validateUsername(self, username):
        regex = re.compile(r"^[a-zA-Z0-9_.-]{4,192}$")
        if regex.match(username) is None:
            return False
        else:
            return True
