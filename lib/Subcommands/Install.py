import base64
import fileinput
import os
import re
import subprocess

from lib.DockerComposeExecutor import DockerComposeExecutor
from lib.Settings import Settings
from lib.Subcommands.CreateDomain import CreateDomain
from lib.Subcommands.InstallApps import InstallApps
from lib.Subcommands.UserCreate import UserCreate
from lib.Subcommands.Wait import Wait
from lib.Tools import paths
from lib.Tools.KeyManager import KeyManager
from lib.UserInformation import UserInformation
from lib.Tools.QueryYesNo import QueryYesNo

class Install:

    def __init__(self):
        self.settings = Settings().getSettings()
        self.key_manager = KeyManager(paths.keys_path)

    def execute(self, *args):

        self.print_welcome_message()
        warning = r"""This software may kill unicorns.

                                                    /
                                                  .7
                                       \       , //
                                       |\.--._/|//
                                      /\ ) ) ).'/
                                     /(  \  // /
                                    /(   J`((_/ \
                                   / ) | _\     /
                                  /|)  \  eJ    L
                                 |  \ L \   L   L
                                /  \  J  `. J   L
                                |  )   L   \/   \
                               /  \    J   (\   /
             _....___         |  \      \   \```
      ,.._.-'        '''--...-||\     -. \   \
    .'.=.'                    `         `.\ [ Y
   /   /                                  \]  J
  Y / Y                                    Y   L
  | | |          \                         |   L
  | | |           Y                        A  J
  |   I           |                       /I\ /
  |    \          I             \        ( |]/|
  J     \         /._           /        -tI/ |
   L     )       /   /'-------'J           `'-:.
   J   .'      ,'  ,' ,     \   `'-.__          \
    \ T      ,'  ,'   )\    /|        ';'---7   /
     \|    ,'L  Y...-' / _.' /         \   /   /
      J   Y  |  J    .'-'   /         ,--.(   /
       L  |  J   L -'     .'         /  |    /\
       |  J.  L  J     .-;.-/       |    \ .' /
       J   L`-J   L____,.-'`        |  _.-'   |
        L  J   L  J                  ``  J    |
        J   L  |   L                     J    |
         L  J  L    \                    L    \
         |   L  ) _.'\                    ) _.'\
         L    \('`    \                  ('`    \
          ) _.'\`-....'                   `-....'
         ('`    \
          `-.___/

Additionally this will consume over 15gb of space.
Are you sure you want to continue?"""
        if not QueryYesNo(warning):
            exit(1)

        hostname = self.get_hostname()
        create_user_domain = False
        user_domain = None
        if self.is_an_ip(hostname):
            create_user_domain, user_domain = self.ask_for_user_domain()

        self.key_manager.generate_keys()
        self.replace_tags(hostname)

        file_path = os.getcwd() + '/environments/compose_files/latest/docker-compose-all.yml'
        docker_compose = DockerComposeExecutor(file_path)
        docker_compose.exec('pull')
        docker_compose.exec('up')

        eyeos_wait = Wait()
        eyeos_wait.execute('wait')

        # Create domain and user
        print('Creating default domain...')
        domain = 'open365.io'
        # domain = input('Enter your domain (default=' + self.settings['general']['default_domain'] + '): ')
        # if not domain:
        #     domain = self.settings['general']['default_domain']
        CreateDomain().execute('create-domain', domain)

        if create_user_domain and user_domain:
            CreateDomain().execute('create-domain', user_domain)

        print('Creating admin user...')
        user_info = UserInformation()
        user_data = user_info.get_default_user_info()
        UserCreate().execute('user-create', *user_data)

        # Finally, install apps
        print('Installing apps...')
        args = ('--user', user_info.user, '--password', user_info.password)

        InstallApps().execute('install-apps', *args)

    def print_welcome_message(self):
        print('\nHi and welcome to the Open365 installer!')
        print('This installer is an early release (Alpha version), so use at your own risk.\n')

    def get_hostname(self):
        hostname = input('Enter your domain or IP: ')
        return hostname

    def is_an_ip(self, hostname):
        is_ip = False
        pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        # Check if hostname is an IP, in such case, ask for a domain
        if pattern.match(hostname):
            is_ip = True
        return is_ip

    def ask_for_user_domain(self):
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        answer = input('Do you have a domain? [y/n]: ').lower()
        while answer not in valid:
            answer = input('Do you have a domain? [y/n]: ').lower()

        if valid[answer]:
            user_domain = input('Enter your domain: ')
            return True, user_domain

        return False, None

    def replace_tags(self, hostname):

        self.prepare_defaults()
        files = self.get_files()

        private_pem = self.key_manager.get_private_pem_base64()
        public_pem = self.key_manager.get_public_pem_base64()
        docker_ip = self.get_docker_ip()

        for file in files:
            with fileinput.FileInput(file, inplace=True) as f:
                for line in f:
                    if '##RAW_FS_PATH##' in line:
                        print(line.replace('##RAW_FS_PATH##', paths.raw_fs), end='')
                    elif '##DATA_PATH##' in line:
                        print(line.replace('##DATA_PATH##', paths.data), end='')
                    elif '##hostname##' in line:
                        print(line.replace('##hostname##', hostname), end='')
                    elif '##docker0##' in line:
                        print(line.replace('##docker0##', docker_ip), end='')
                    elif '##RESOLV_PATH##' in line:
                        print(line.replace('##RESOLV_PATH##', paths.resolv_conf_file), end='')
                    elif '##DOCKER_VOLS##' in line:
                        print(line.replace('##DOCKER_VOLS##', paths.docker_volumes), end='')
                    elif '##HOSTS##' in line:
                        print(line.replace('##HOSTS##', paths.hosts), end='')
                    elif '##PRIVATE_PEM##' in line:
                        print(line.replace('##PRIVATE_PEM##', private_pem), end='')
                    elif '##PUBLIC_PEM##' in line:
                        print(line.replace('##PUBLIC_PEM##', public_pem), end='')
                    else:
                        print(line, end='')

    def prepare_defaults(self):
        if not os.path.exists('environments/envars'):
            os.mkdir('environments/envars')
        if not os.path.exists(paths.raw_fs):
            os.mkdir(paths.raw_fs)
        if not os.path.exists(paths.data):
            os.mkdir(paths.data)

        os.system('cp defaults/envars/* environments/envars/')
        os.system('cp defaults/compose_files/* environments/compose_files/latest/')
        os.system('cp defaults/settings.cfg ./')

        sestatus = subprocess.check_output("sestatus | grep 'SELinux status' | grep enabled | wc -l", shell=True)
        sestatus = sestatus.decode("utf-8").rstrip("\n")
        if sestatus.find('1') > -1:
            # SELinux is activated!
            print('Fix selinux')
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.raw_fs)
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.data)
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.hosts)
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.resolv_conf_file)
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.docker_volumes + '/ssl')
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.docker_volumes + '/multidocker-info')
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.docker_volumes + '/license')
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.docker_volumes + '/docker-swarm')
            os.system('chcon -Rt svirt_sandbox_file_t ' + paths.docker_volumes + '/signup')

    def get_files(self):
        tmp = os.listdir('environments/envars')
        files = ['environments/envars/' + file for file in tmp]
        files.append('environments/compose_files/latest/docker-compose-all.yml')
        files.append('settings.cfg')
        return files

    def get_docker_ip(self):
        docker_ip = subprocess.check_output("ip route | grep docker0 | awk {'print $9'}", shell=True)
        docker_ip = docker_ip.decode("utf-8").strip('\n')
        if not docker_ip:
            docker_ip = '172.17.0.1'
        return docker_ip
