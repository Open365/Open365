from lib.Wrappers.ArgumentParser import ArgumentParser
from lib.Wrappers.Logger import Logger
from lib.Settings import Settings
from lib.DomainManagement.Domain import Domain
import re
import sys


class CreateDomain:

    def __init__(self):
        self.settings = Settings().getSettings()
        self.logger = Logger(__name__)
        self.domain = Domain()

    def execute(self, *args):
        args = self._parse_arguments(*args)
        args.domain[0] = args.domain[0].lower()
        if self.domain.domain_exists(args.domain[0]) is True:
            self.logger.error("Domain already exists")
            sys.exit(1)
        regex = "^[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\.[a-zA-Z]{2,})$"
        pattern = re.compile(regex)
        if not pattern.match(args.domain[0]):
            self.logger.error("The domain you provided is not valid!")
            sys.exit(1)
        self.domain.create_domain(args.domain[0])

    def _parse_arguments(self, command_name, *args):
        parser = ArgumentParser(description='Domains creation',
                                prog='eyeos ' + command_name)
        parser.add_argument('domain', metavar='DOMAIN', nargs=1,
                            help='DNS name of the domain to create')
        args = parser.parse_args(args)
        return args
