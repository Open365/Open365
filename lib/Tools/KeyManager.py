import os
import base64

class KeyManager:

    def __init__(self, path):
        self.path = path
        self.public_key = None
        self.private_key = None

    def generate_keys(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        os.system('openssl genrsa -out ' + self.path + '/mykey.pem 512')
        os.system('openssl rsa -in ' + self.path + '/mykey.pem -pubout -out ' + self.path + '/pub.pem')

    def get_private_pem_base64(self):
        with open(self.path + "/mykey.pem", "rb") as key_file:
            encoded_string = base64.b64encode(key_file.read())
        return encoded_string.decode("utf-8")

    def get_public_pem_base64(self):
        with open(self.path + "/pub.pem", "rb") as key_file:
            encoded_string = base64.b64encode(key_file.read())
        return encoded_string.decode("utf-8")
