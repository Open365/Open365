import warnings as global_warnings

from lib.Settings import Settings


class Warnings:
    def __init__(self, *, warnings=None):
        self.warnings = warnings or global_warnings

    def configure(self, *, settings=None):
        action = (settings or Settings().getSettings())['logs']['warning_action']

        self.warnings.filterwarnings(action)
        self.warnings.formatwarning = self._format_warning

    def _format_warning(self, message, category, filename, lineno, line=None):
        return "{cat}: {msg}\n  Warned inside call made in {file}:{line}\n".format(cat=category.__name__,
                                                                                   msg=message,
                                                                                   file=filename,
                                                                                   line=lineno)
