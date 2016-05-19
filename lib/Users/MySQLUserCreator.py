# yum install mysql-devel python3-devel # deps de mysqlclient
# pip3 install mysqlclient # afegir a requirements.txt

import hashlib
import MySQLdb
from lib.Settings import Settings
from lib.Wrappers.Logger import Logger


class MySQLUserCreator():

    def __init__(self):
        self.settings = Settings().getSettings()
        self.logger = Logger(__name__)

    def _get_db_credentials(self, username, domain):
        if self.settings['general']['multitenant'] == "true":
            username = username + "_" + domain
        m = hashlib.sha256()
        salted_user = username + self.settings['mysql']['user_salt']
        m.update(str.encode(salted_user))
        mysqlPassword = m.hexdigest()
        if self.settings['general']['multitenant'] == "true":
            self.logger.debug("Creating db and user for mysql with multitenant.")
            m.update(str.encode(username))
            dbname = m.hexdigest()
            username = dbname[0:16]
            return (username + "_dbv2", username, mysqlPassword)

        return (username + "_db", username, mysqlPassword)

    def create_user(self, username, domain):
        print("Creating db for", username, domain)
        dbname, mysqlUsername, mysqlPassword = self._get_db_credentials(username, domain)

        db = MySQLdb.connect(host=self.settings['mysql']['host'],
                             user="root",
                             passwd=self.settings['mysql']['root_password'],
                             db="mysql")

        print("Connected to mysql db")
        with db, db.cursor() as cur:

            create_stmt = "CREATE USER %(username)s@'%%' IDENTIFIED BY %(password)s;"
            self.logger.debug("Creating mysql user " + mysqlUsername)
            cur.execute(create_stmt, {'username': mysqlUsername, 'password': mysqlPassword})

            self.logger.debug("Creating db " + dbname + " with user " + mysqlUsername)
            cur.execute("CREATE DATABASE `" + dbname + "`;")

            self.logger.debug("Granting privileges on " + dbname + " to user " + mysqlUsername)
            cur.execute("GRANT ALL PRIVILEGES ON `" + dbname + "`.* TO %(username)s@'%%';",
                        {'username': mysqlUsername})
            cur.execute("FLUSH PRIVILEGES;")

            db.commit()
        print("Created db")
