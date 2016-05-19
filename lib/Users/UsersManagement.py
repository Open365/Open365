from lib.Wrappers.Logger import Logger
from lib.Users.UsersProvider import UsersProvider
from lib.Settings import Settings
from lib.Users.MySQLUserCreator import MySQLUserCreator
from lib.Users.MongoForgotPassword import MongoForgotPassword
from lib.FS.FileSystem import FileSystem

from lib.EyeosApi.Login import Login
from lib.EyeosApi.Logout import Logout


class UsersManagement:

    def __init__(self, usersProvider=None):
        self.logger = Logger(__name__)
        self.userProvider = usersProvider or UsersProvider()
        self.settings = Settings().getSettings()
        self.mysql = MySQLUserCreator()
        self.fs = FileSystem()
        self.mongoForgotPass = MongoForgotPassword()

    def createUser(self, args):
        with self.userProvider.connect() as usersClient:
            if self.settings['general']['multitenant'] == "true":
                email = args.user[0] + '@' + args.domain
                username = args.user[0] + '@' + args.domain
            else:
                email = args.user[0] + '@' + self.settings['email']['domain']
                username = args.user[0]
            ret = usersClient.createUser(username, args.firstname, args.surname, args.password, email)
            if ret:
                self.logger.info("User created")
                self.mysql.create_user(args.user[0], args.domain)
                self.fs.create_skel(args.user[0], args.domain)
                self.mongoForgotPass.insert_user(args.user[0], args.email, args.domain)

                login_api = Login()
                logout_api = Logout()

                eyeos_card = login_api.authenticate(args.user[0], args.password, args.domain)
                self.logger.info("Logged in as user")
                logout_api.logout(eyeos_card)

            return ret

    def _send_welcome_email(self, args, email):
        with open('lib/Users/welcome_email/text', 'r') as content:
            plain_content = content.read()
        with open('lib/Users/welcome_email/html.html', 'r') as content:
            html_content = content.read()
        with open('lib/Users/welcome_email/subject', 'r') as content:
            subject = content.read()

        email_from = email
        email_to = email
        smtp_host = self.settings['email']['smtp_host']

    def deleteUser(self, args):
        try:
            with self.userProvider.connect() as usersClient:
                usersClient.deleteUser(args.user[0])
                self.logger.info("Delete user")
                return True
        except Exception as e:
            self.logger.error("Could not delete user")
            return False

    def findUser(self, args):
        try:
            with self.userProvider.connect() as usersClient:
                usernames = usersClient.findUser(args.user[0])
                self.logger.info("Found {0} users matching '{1}'".format(len(usernames), args.user[0]))
                for user in usernames:
                    print(user)
                return True
        except Exception as e:
            self.logger.info("Does not match any entries")
            return False
