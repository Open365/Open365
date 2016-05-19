import getpass
from lib.Settings import Settings


class UserInformation:

    def __init__(self):
        self.settings = Settings().getSettings()
        self.user = None
        self.firstname = None
        self.surname = None
        self.password = None
        self.repassword = None
        self.domain = None
        self.email = None

    def get_user_info(self):
        print("\nLet's create a user...")
        self.user = input('Username: ')
        self.firstname = input('Firstname: ')
        self.surname = input('Surname: ')
        if not self.surname:
            self.surname = 'default'
        self.password = getpass.getpass('Passowrd: ')
        self.repassword = getpass.getpass('Reenter password: ')
        while self.password != self.repassword:
            print('Password does not match, try again...')
            self.password = getpass.getpass('Password: ')
            self.repassword = getpass.getpass('Reenter password: ')

        self.domain = input('Domain (default ' + self.settings['general']['default_domain'] + '): ')
        if not self.domain:
            self.domain = self.settings['general']['default_domain']

        self.email = input('Email: ')

        return self.user, '--firstname', self.firstname, '--surname', self.surname, '--password', self.password, '--domain', self.domain, '--email', self.email

    def get_default_user_info(self):
        self.user = 'eyeos'
        self.firstname = 'eyeos'
        self.surname = 'eyeos'
        print('Enter admin password')
        self.password = getpass.getpass('Passowrd: ')
        self.repassword = getpass.getpass('Reenter password: ')
        while self.password != self.repassword:
            print('Password does not match, try again...')
            self.password = getpass.getpass('Password: ')
            self.repassword = getpass.getpass('Reenter password: ')

        self.domain = self.settings['general']['default_domain']

        self.email = 'eyeos@'+self.settings['general']['default_domain']

        return self.user, '--firstname', self.firstname, '--surname', self.surname, '--password', self.password, '--domain', self.domain, '--email', self.email
