from warnings import filterwarnings
from lib.Settings import Settings
from lib.Wrappers.Logger import Logger
import MySQLdb
filterwarnings('ignore', category=MySQLdb.Warning)


class MailDomain:
    def __init__(self):
        self.logger = Logger(__name__)
        self.settings = Settings().getSettings()

    def create_domain(self, domain):
        self._prepare_db()
        self._prepare_table()
        self._insert_domain(domain)

    def domain_exists(self, domain):
        self._prepare_db()
        self._prepare_table()
        db = MySQLdb.connect(host=self.settings['email']['dbhost'],
                             user=self.settings['email']['dbuser'],
                             passwd=self.settings['email']['dbpwd'],
                             db=self.settings['email']['dbname'])

        with db, db.cursor() as cur:
            cur.execute("SELECT * FROM domains WHERE domain='" + domain + "';")
            data = cur.fetchone()
            if data is not None and data[0] == domain:
                self.logger.debug('The domain ' + domain + ' exists.')
                return True
            else:
                self.logger.debug('The domain ' + domain + ' don\'t exists.')
                return False

    def _prepare_db(self):
        db = MySQLdb.connect(host=self.settings['mysql']['host'],
                             user="root",
                             passwd=self.settings['mysql']['root_password'],
                             db="mysql")

        with db, db.cursor() as cur:
            dbname = self.settings['email']['dbname']
            query = "CREATE DATABASE IF NOT EXISTS `" + dbname + "`;"
            self.logger.debug('Creating database ' + dbname)
            cur.execute(query)

            username = self.settings['email']['dbuser']
            mysqlpassword = self.settings['email']['dbpwd']

            self.logger.debug("Granting privileges on " + dbname + " to user " + username)
            cur.execute("GRANT ALL PRIVILEGES ON `" + dbname + "`.* TO %(username)s@'%%' IDENTIFIED BY %(password)s;",
                        {'username': username, 'password': mysqlpassword})
            cur.execute("FLUSH PRIVILEGES;")

    def _prepare_table(self):
        db = MySQLdb.connect(host=self.settings['email']['dbhost'],
                             user=self.settings['email']['dbuser'],
                             passwd=self.settings['email']['dbpwd'],
                             db=self.settings['email']['dbname'])

        with db, db.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS "
                        "domains (domain varchar(50) NOT NULL,PRIMARY KEY (domain) )ENGINE=MyISAM;")

    def _insert_domain(self, domain):
        db = MySQLdb.connect(host=self.settings['email']['dbhost'],
                             user=self.settings['email']['dbuser'],
                             passwd=self.settings['email']['dbpwd'],
                             db=self.settings['email']['dbname'])

        with db, db.cursor() as cur:
            self.logger.info('Creating domain ' + domain)
            cur.execute('INSERT INTO domains(domain) VALUES(\"' + domain + '\");')
