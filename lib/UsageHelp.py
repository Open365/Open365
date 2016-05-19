import fileinput
import os
import re
import textwrap
import sys
import lib.Tools.Casify as Casify


class UsageHelp:
    def __init__(self):
        pass

    def show(self):
        subcommands = self._get_subcommands_list()

        a = textwrap.dedent('''
        Usage: sudo ./open365 SUBCOMMAND [args...]

        SUBCOMMAND is one of:
        ''')
        a += "\t" + "\n\t".join(subcommands)
        a += textwrap.dedent('''

        You can get help for a subcommand with

        \t sudo ./open365 SUBCOMMAND --help
        ''')
        print(a)

    def _get_subcommands_list(self):
        files = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Subcommands'))
        return sorted(Casify.to_dash_case(file[:-3]) for file in files if file.endswith('.py'))

    def _get_profiles_list(self):
        profiles_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     '..',
                                     'environments',
                                     'compose_files',
                                     'latest')
        all_files = (os.path.join(profiles_path, file) for file in os.listdir(profiles_path) if file.endswith('.yml'))
        regex = re.compile('^include:$')
        files = []
        with fileinput.input(all_files) as line_iter:
            for line in line_iter:
                if regex.search(line):
                    files.append(os.path.basename(line_iter.filename())[:-4])
                    line_iter.nextfile()
        return sorted(files)


if __name__ == '__main__':
    # used directly to extract the Subcommands list to generate bash_completion helper
    usage = UsageHelp()
    what = 'subcommands'
    if len(sys.argv) == 2:
        what = sys.argv[1]
    if what == 'subcommands':
        print(*usage._get_subcommands_list())
    elif what == 'profiles':
        print(*usage._get_profiles_list())
