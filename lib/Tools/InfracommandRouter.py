from lib.Tools.Casify import to_dash_case
from lib.Tools.InstanceCollector import InstanceCollector
from lib.Tools.InstanceResolver import InstanceResolver
from lib.Wrappers.ArgumentParser import ArgumentParser


class InfracommandRouter:
    def __init__(self,
                 subcommands_path,
                 description,
                 arg_name,
                 arg_help,
                 *,
                 instance_collector=None,
                 instance_resolver=None):
        self.subcommands_path = subcommands_path
        self.description = description
        self.arg_name = arg_name
        self.arg_help = arg_help

        self.instance_collector = instance_collector or InstanceCollector(instantiate=False)
        self.instance_resolver = instance_resolver or InstanceResolver()

    def execute(self, *args):
        # kind of ugly, but pass only the first 2 arguments ('publish' and TYPE), so ArgumentParser can parse if
        # it is the right type (or --help and print the help message nicely formatted). If we pass all the parameters
        # it will bitch about 'unrecognized parameters' when it is the TYPE PublishCommand the one who has to parse
        # the remainding params
        arguments = self._parse_arguments(*args[0:2])
        instance = self.instance_resolver.resolve(getattr(arguments, self.arg_name),
                                                  self.subcommands_path.replace('/', '.'))
        instance.execute(*args)

    def _parse_arguments(self, command_name, *args):
        available_types = self._get_list_of_subcommands()
        parser = ArgumentParser(description=self.description,
                                prog='eyeos ' + command_name)
        parser.add_argument(self.arg_name, metavar=self.arg_name.upper(), choices=available_types,
                            help=self.arg_help + ': {0}'.format(available_types))
        args = parser.parse_args(args)
        return args

    def _get_list_of_subcommands(self):
        return [to_dash_case(n.__name__) for n in self.instance_collector.collect(self.subcommands_path)]
