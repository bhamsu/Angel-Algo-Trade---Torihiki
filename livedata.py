# Importing required packages
import os
from dotenv import load_dotenv
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger

class get_livedata:

    def __init__(self, client_code, feed_token):
        self.configure()
        self.correlation_id = "abc123"
        self.action = 1
        self.mode = 1
        self.token_list = [
            {
                "exchangeType": 1,
                "tokens": ["26009"]
            }
        ]
        # retry_strategy=0 for simple retry mechanism
        self.sws = SmartWebSocketV2(os.getenv('secret_key'), os.getenv('api_key'), client_code, feed_token, max_retry_attempt = 2, retry_strategy = 0, retry_delay = 10, retry_duration = 30)
        print("SmartWebSocket connection established!")
        # retry_strategy=1 for exponential retry mechanism
        # sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)

    @staticmethod
    def configure():
        load_dotenv()
        print(".env variables loaded successfully...")

    @staticmethod
    def on_data(wsapp, message):
        logger.info("Ticks: {}".format(message))
        # close_connection()

    @staticmethod
    def on_control_message(wsapp, message):
        logger.info(f"Control Message: {message}")

    def on_open(self, wsapp):
        logger.info("on open")
        some_error_condition = False
        if some_error_condition:
            error_message = "Simulated error"
            if hasattr(wsapp, 'on_error'):
                wsapp.on_error("Custom Error Type", error_message)
        else:
            self.sws.subscribe(self.correlation_id, self.mode, self.token_list)
            # sws.unsubscribe(correlation_id, mode, token_list1)

    @staticmethod
    def on_error(wsapp, error):
        logger.error(error)

    @staticmethod
    def on_close(wsapp):
        logger.info("Close")

    def close_connection(self):
        self.sws.close_connection()

    def __call__(self, *args, **kwargs):
        # Assign the callbacks.
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close
        self.sws.on_control_message = self.on_control_message

        self.sws.connect()

    def __delete__(self):
        print("'__delete__' destructor called!!")