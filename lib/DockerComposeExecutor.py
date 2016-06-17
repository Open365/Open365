import os
import subprocess as global_subprocess


class DockerComposeExecutor:
    def __init__(self, file, subprocess=None):
        self.file = file
        self.cwd = os.getcwd()
        self.subprocess = subprocess or global_subprocess
        self.project_name = "eyeos"

    def exec(self, operation, components=[]):
        command_args = {
            'up': ['up', '-d'],
            'rm': ['rm', '--force', '-v']
        }
        try:
            args = command_args[operation]
        except KeyError:
            args = [operation]

        args = (['docker-compose',
                 '--file',
                 self.file,
                 '-p',
                 self.project_name,
                 ] +
                args +
                components)
        print('Executing: {0}'.format(args))
        try:
            new_env = os.environ.copy()
            new_env['DOCKER_CLIENT_TIMEOUT'] = '300'
            new_env['COMPOSE_HTTP_TIMEOUT'] = '300'
            self.subprocess.check_call(args, cwd=self.cwd, env=new_env)
            print("Command {0} exited successfully".format(args))
        except global_subprocess.CalledProcessError as e:
            print("Command {0} failed with exit status {1}".format(e.cmd, e.returncode))
            raise
