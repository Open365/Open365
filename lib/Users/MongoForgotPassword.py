from lib.Settings import Settings
from pymongo import MongoClient


class MongoForgotPassword:

    def __init__(self, injected_mongo_client=None):
        self.settings = Settings().getSettings()
        self.forgot_password = injected_mongo_client or MongoClient(
            Settings().getServiceIp('mongo')
        ).eyeos.forgotpassword

    def insert_user(self, username, email, domain):
        self.forgot_password.insert_one({
            "username": username + '@' + domain,
            "personal_email": email
        })
