from lib.Errors.SubcommandNotFoundError import SubcommandNotFoundError
from lib.Tools.InstanceResolver import InstanceResolver
from lib.UsageHelp import UsageHelp
from lib.Wrappers.Logger import Logger


class SubcommandRouter:
    def __init__(self, devenvExecutor=None, instanceResolver=None):
        self.instanceResolver = instanceResolver or InstanceResolver()
        self.logger = Logger(__name__)

    def route(self, *args):
        if args[0] in ('help', '-h', '--help'):
            if len(args) == 1:
                usage = UsageHelp()
                usage.show()
                return
            else:
                args = list(args)
                args[0] = args[1]
                args[1] = '--help'

        try:
            instance = self.instanceResolver.resolve(args[0])
            instance.execute(*args)
        except SubcommandNotFoundError:
            usage = UsageHelp()
            usage.show()
