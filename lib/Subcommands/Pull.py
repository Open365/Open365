import os

from lib.DockerComposeExecutor import DockerComposeExecutor
from lib.Tools import paths


class Pull:
    def __init__(self, manager_factory=None):
        pass

    def execute(self, *args):
        file_path = os.getcwd() + '/environments/compose_files/latest/docker-compose-all.yml'
        docker_compose = DockerComposeExecutor(file_path)
        docker_compose.exec('pull')

