import this
from tradingAPI import TradingApi
import time, json

date = str(int(round(time.time() * 1000)))
activeAPIKey = 0

apiKeyUsage = 0
apikeysAlpha = ["EBYN9X417QJPRW0H","69VVOVMN5HZSC0MR","91T1NXYG5ZKCC6ZH","LV7YQS6FE4ZQACD4","DM20V7IUNGGUARB2"]

def getKey():
        if(apiKeyUsage >= 5):
            global activeAPIKey
            activeAPIKey = (activeAPIKey+1)%len(apikeysAlpha)
        return apikeysAlpha[activeAPIKey]

class AlphavantageAPI():

    def getCompanyOverview(symbol): 
        url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey="+getKey()
        data = TradingApi.apiRequest(url)
        return data 
    

    