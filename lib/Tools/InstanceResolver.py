import importlib
from lib.Errors.SubcommandNotFoundError import SubcommandNotFoundError
import lib.Tools.Casify as Casify


class InstanceResolver:
    def __init__(self, instantiate=True):
        self.instantiate = instantiate

    def resolve(self, name, path='lib.Subcommands'):
        class_name = Casify.to_pascal_case(name)
        module_name = path + "." + class_name
        try:
            mod = importlib.import_module(module_name)
            cls = getattr(mod, class_name)
        except ImportError as e:
            if e.name != module_name:
                raise
            else:
                raise SubcommandNotFoundError(name) from e
        if self.instantiate:
            return cls()
        else:
            return cls
