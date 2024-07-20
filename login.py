# Importing required packages
import os
import pyotp
from logzero import logger
from dotenv import load_dotenv
from SmartApi import SmartConnect


class angel_login:
    def __init__(self, username, password):
        self.username = username
        self.pwd = password
        self.feedToken = None
        self.configure()

        self.smartApi = SmartConnect(os.getenv('api_key'))
        print("Smart API Connected Successfully...")

    @staticmethod
    def configure():
        load_dotenv()
        print(".env variables loaded successfully...")

    def authentication(self):

        try:
            token = os.getenv('totp_token')
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        correlation_id = "abcde"
        login_status = self.smartApi.generateSession(self.username, self.pwd, totp)

        if not login_status['status']:
            print("Login Error!!")
            logger.error(login_status)

        else:
            # login api call
            # logger.info(f"You Credentials: {data}")
            authToken = login_status['data']['jwtToken']
            refreshToken = login_status['data']['refreshToken']

            # fetch the feed-token
            self.feedToken = self.smartApi.getfeedToken()
            print(f"Generated Feed Token: {self.feedToken}")

            # fetch User Profile
            res = self.smartApi.getProfile(refreshToken)
            self.smartApi.generateToken(refreshToken)
            res = res['data']['exchanges']
            print(f"Login to Angel Broking Trading Account {self.username} Successful!!")

    def __call__(self, *args, **kwargs):
        self.authentication()
        return self.username, self.feedToken

    def __delete__(self):
        print("'__delete__' destructor called!!")