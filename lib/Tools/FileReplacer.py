import fileinput
import glob
import os
import re


class FileReplacer:
    def __init__(self):
        pass

    def replace(self, patterns, frm, to):
        regex = re.compile(frm)
        if isinstance(patterns, str):
            patterns = [patterns]

        input_files = []

        for pattern in patterns:
            input_files += glob.glob(pattern)

        input_files = [file for file in input_files if not os.path.isdir(file)]
        with fileinput.input(files=input_files, inplace=True) as line_iter:
            for line in line_iter:
                print(regex.sub(to, line), end="")
