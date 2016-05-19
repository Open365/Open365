from lib.Wrappers.ArgumentParser import ArgumentParser
from lib.DockerManagerFactory import DockerManagerFactory


class Pull:
    def __init__(self, manager_factory=None):
        self.manager_factory = manager_factory or DockerManagerFactory()

    def execute(self, *args):
        arguments = self._parse_arguments(*args)
        manager = self.manager_factory.get_manager(arguments.version)
        manager.pull(arguments.components)

    def _parse_arguments(self, command_name, *args):
        parser = ArgumentParser(description='Pulls the desired containers',
                                prog='eyeos ' + command_name)
        parser.add_argument('-v', '--version', metavar='VERSION', type=str,
                            help='pull the version VERSION', default=ArgumentParser.DEFAULT_VERSION)
        # parser.add_argument('-n', '--node', metavar='NODE', type=str, default=['all'], action='append',
        #                     help='pull in NODE only (this flag can be specified multiple times)')
        parser.add_argument('components', metavar='COMPONENT', nargs='*', default=ArgumentParser.DEFAULT_COMPONENTS,
                            help='which component(s) to pull')
        args = parser.parse_args(args)
        return args
