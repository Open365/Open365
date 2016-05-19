class FileUtils:
    def __init__(self):
        pass

    def get_contents(self, filename):
        with open(filename, 'r') as fd:
            return fd.read()
