import pandas as pd

class get_data:
    def __init__(self, smartApi):
        self.smartApi = smartApi

    def historical_data(self, exchange, token, from_date, to_date, timeperiod):
        """
            Function to fetch historical data and return it as a Pandas DataFrame.
        """
        try:
            historicParam = {
                "exchange": exchange,
                "symboltoken": token,
                "interval": timeperiod,
                "fromdate": from_date,
                "todate": to_date
            }
            api_response = self.smartApi.getCandleData(historicParam)
            data = api_response['data']
            columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.DataFrame(data, columns = columns)
            df['DateTime'] = pd.to_datetime(df['DateTime'])
            df.set_index('DateTime', inplace = True)
            return df
        except Exception as e:
            print("Historic Api failed: {}".format(e))

    def __delete__(self):
        print("'__delete__' destructor called!!")