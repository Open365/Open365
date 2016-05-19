import os

from lib.DockerComposeExecutor import DockerComposeExecutor
from lib.Tools import paths


class Destroy:

    def __init__(self):
        pass

    def execute(self, *args):
        file_path = os.getcwd() + '/environments/compose_files/latest/docker-compose-all.yml'
        docker_compose = DockerComposeExecutor(file_path)
        docker_compose.exec('kill')
        docker_compose.exec('rm')

        os.system('rm -rf ' + paths.raw_fs)
        os.system('rm -rf ' + paths.data)
