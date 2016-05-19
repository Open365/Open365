import argparse

class ArgumentParser:
    DEFAULT_VERSION = 'last stable'

    def __init__(self, *args, argument_parser=None, version_provider=None, **kwargs):
        self.parser = argument_parser or argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                                 *args,
                                                                 **kwargs)
        self._common_args()

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def parse_args(self, args):
        arguments = self.parser.parse_args(args)
        if 'version' in arguments and arguments.version == self.DEFAULT_VERSION:
            arguments.version = '1.0'

        return arguments

    def _common_args(self):
        self.parser.add_argument('-S', '--settings', metavar='SETTINGS', type=str,
                                 help='Path to the settings file.', default="settings.cfg")
