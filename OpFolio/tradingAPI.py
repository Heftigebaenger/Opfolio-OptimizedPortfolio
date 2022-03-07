
#from stock import Stock
import requests
from abc import ABC,abstractmethod

class TradingApi(ABC):
    @staticmethod
    def apiRequest(url):
        r = requests.get(url)
        data = r.json()
        return data

    @staticmethod
    @abstractmethod
    def getInformations(symbol):
        pass

    @staticmethod
    @abstractmethod
    def getToday(symbol):
        pass

    @staticmethod
    @abstractmethod
    def getLastMonth(symbol):
        pass
    
    @staticmethod
    @abstractmethod
    def getLast6Month(symbol):
        pass

    @staticmethod
    @abstractmethod
    def getLastYear(symbol):
        pass