from tradingAPI import TradingApi
import time, json

apikeyAmeri = "96I1BNR5FXVTRTMNASI2Z7IPYG07MG9P"
date = str(int(round(time.time() * 1000)))


class AmeriTradeAPI(TradingApi):
    @staticmethod
    def getToday(symbol):
        today = int(round(time.time() * 1000))- 10000
        yesterday = today - 86400000
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=day&period=1&frequencyType=minute&frequency=5&endDate="+str(today)+"&startDate="+str(yesterday)+"&needExtendedHoursData=false"
        data = TradingApi.apiRequest(url)
        try:
            if data["candles"][-1]["open"] == 0:
                data["candles"].pop()
        except :
            print("No candle")
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=day&period=1&frequencyType=minute&frequency=5&endDate="+str(today)+"&needExtendedHoursData=false"
        data = TradingApi.apiRequest(url)
        return data

    @staticmethod
    def getInformations(symbol):
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/quotes?apikey=" + apikeyAmeri
        data = TradingApi.apiRequest(url)
        data = data[symbol]
        return data

    @staticmethod
    def getLastMonth(symbol):
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=month&period=6&frequencyType=daily&frequency=1&endDate="+date+"&needExtendedHoursData=true"
        data = TradingApi.apiRequest(url)
        return data    
    
    @staticmethod
    def getLastYear(symbol):
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=year&period=1&frequencyType=weekly&frequency=1&needExtendedHoursData=true"
        data = TradingApi.apiRequest(url)
        return data
    
    @staticmethod
    def getLast6Month(symbol):
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=month&period=6&frequencyType=daily&frequency=1&endDate="+date+"&needExtendedHoursData=true"
        data = TradingApi.apiRequest(url)
        return data

    def getLast5Years(symbol):
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=year&period=5&frequencyType=monthly&frequency=1&needExtendedHoursData=true"
        data = TradingApi.apiRequest(url)
        return data

    def getLast5YearsDaily(symbol):
        url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=year&period=5&frequencyType=daily&frequency=1"
        data = TradingApi.apiRequest(url)
        return data