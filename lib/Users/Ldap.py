from ldap3 import Server, Connection, ALL, SUBTREE
import ldap3 as ldap
from lib.Wrappers.Logger import Logger
from lib.Settings import Settings
import hashlib
import base64


class Ldap:

    class __Ldap:
        ldap = None

        def __init__(self, settings=None):
            self.settings = settings or Settings()
            self.logger = Logger(__name__)

        def getInstance(self):
            settings = self.settings.getSettings()
            user = settings['ldap']['admin_ldap_username']
            password = settings['ldap']['admin_ldap_password']
            host = self.settings.getServiceIp('ldap')
            self.logger.debug("Connecting to " + host + " with user " + user)
            self.dn_base = settings['ldap']['ldap_cn_base']
            server = Server(host, get_info=ALL)
            self.ldapClient = Connection(server, user=user, password=password, raise_exceptions=True)
            try:
                self.ldapClient.bind()
            except ldap.LDAPSocketOpenError as e:
                self.logger.error("Could not connect to LDAP - SocketOpenError: " + str(e))
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self.ldapClient.unbind()

        def disconnect(self):
            self.ldapClient.unbind()

        def createUser(self, user, firstname, lastname, password, email):
            password = password.encode('utf-8')
            hashPassword = hashlib.md5()
            hashPassword.update(password)
            password = base64.b64encode(hashPassword.digest())
            dn = "cn=" + user + "," + self.dn_base
            attrs = {}
            attrs['objectClass'] = ['inetOrgPerson', 'person', 'top', 'organizationalPerson']
            attrs['cn'] = user
            attrs['userPassword'] = "{MD5}" + password.decode('utf-8')
            attrs['sn'] = lastname
            attrs['givenName'] = firstname
            attrs['mail'] = email
            try:
                self.ldapClient.add(dn, attributes=attrs)
                self.logger.info(self.ldapClient.result)
            except ldap.LDAPEntryAlreadyExistsResult:
                self.logger.error("Could not create user, duplicated " + user)
                return False
            except Exception as e:
                self.logger.error("Could not create user: " + str(e))
                return False

            return True

        def deleteUser(self, user):
            deleteDN = "cn="+user+","+self.dn_base
            self.ldapClient.delete(deleteDN)
            return True

        def findUser(self, user):
            self.ldapClient.search(search_base=self.dn_base,
                                   search_filter='(&(objectClass=inetOrgPerson)(cn=' + user + '))',
                                   search_scope=SUBTREE,
                                   attributes=['cn'])

            usernames = []
            for result in self.ldapClient.response:
                cn = result['attributes']['cn'][0]
                if cn:
                    usernames.append(cn)

            return usernames

    instance = None

    def __init__(self):
        if not Ldap.instance:
            Ldap.instance = Ldap.__Ldap()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def reset(self):
        Ldap.instance = None
