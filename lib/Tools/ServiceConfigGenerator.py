import json as global_json
import tempfile as global_tempfile


class ServiceConfigGenerator:
    def __init__(self, tempfile=None, json=None):
        self.tempfile = tempfile or global_tempfile
        self.json = json or global_json

    def generate_change_log_level(self, log_level):
        with self.tempfile.NamedTemporaryFile(mode='wt', prefix='tmp.eyeos-change-log-level', delete=False) as fd:
            filename = fd.name
            self.json.dump({
                'levels': {
                    '[all]': log_level
                }
            }, fd)

        return filename

    def generate_stdout_log_config(self, enabled):
        with self.tempfile.NamedTemporaryFile(mode='wt', prefix='tmp.eyeos-stdout-log-conf', delete=False) as fd:
            filename = fd.name
            self.json.dump({
                'stdout': {
                    'enabled': enabled
                }
            }, fd)

        return filename
