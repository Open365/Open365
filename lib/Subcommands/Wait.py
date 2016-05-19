from lib.Wrappers.ArgumentParser import ArgumentParser
from lib.Tools.WaitForEyeos import WaitForEyeos


class Wait:
    def __init__(self, waiter=None):
        self.waiter = waiter or WaitForEyeos()

    def execute(self, *args):
        arguments = self._parse_arguments(*args)
        try:
            self.waiter.wait(arguments.timeout)
        except TimeoutError as e:
            exit(e)

    def _parse_arguments(self, command_name, *args):
        parser = ArgumentParser(description='Blocks until eyeos is ready',
                                prog='eyeos ' + command_name)
        parser.add_argument('--timeout', metavar='TIMEOUT', default='inf', nargs='?', type=float,
                            help="Maximum wait time. Wait time might be longer than specified because"
                                 "DNS requests block.")
        args = parser.parse_args(args)
        return args
