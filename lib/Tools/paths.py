import os


base_path = os.getcwd()
raw_fs = base_path + '/rawFS'
data = base_path + '/data'
hosts = base_path + '/environments/compose_files/latest/hosts'
resolv_conf_file = base_path + '/environments/compose_files/latest/resolv.conf'
docker_volumes = base_path + '/environments/volumes'
keys_path = base_path + '/keys'