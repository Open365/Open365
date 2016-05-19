import glob as global_glob
import os
from lib.Tools.InstanceResolver import InstanceResolver


class InstanceCollector:
    def __init__(self, instantiate=True, *, instance_resolver=None, glob=None):
        self.instance_resolver = instance_resolver or InstanceResolver(instantiate)
        self.glob = glob or global_glob

    # this returns an iterator!
    def collect(self, path):
        for filename in self.glob.iglob(os.path.join(path, '*.py')):
            modparts = filename.replace('/', '.').split('.')[:-1]
            clsname = modparts[-1]
            folder = ".".join(modparts[:-1])
            yield self.instance_resolver.resolve(clsname, folder)
