from lib.Wrappers.Logger import Logger
from lib.Users.Ldap import Ldap


class UsersProvider:
    def __init__(self):
        self.logger = Logger(__name__)
        self.ldap = Ldap()

    def connect(self):
        return self.ldap.getInstance()
