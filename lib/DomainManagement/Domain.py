from lib.Wrappers.Logger import Logger
from lib.DomainManagement.MailDomain import MailDomain


class Domain:
    def __init__(self):
        self.logger = Logger(__name__)
        self.mail = MailDomain()

    def create_domain(self, domain):
        self.mail.create_domain(domain)

    def domain_exists(self, domain):
        return self.mail.domain_exists(domain)
