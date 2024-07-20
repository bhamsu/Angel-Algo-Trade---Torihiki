from login import angel_login
from history import get_data
from livedata import get_livedata
from datetime import datetime, timedelta

angelLogin = angel_login(username = 'A694852', password = '1965')
client, feed_token = angelLogin.__call__()
smartApi = angelLogin.smartApi

