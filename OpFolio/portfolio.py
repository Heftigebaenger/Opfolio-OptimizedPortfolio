from logging import error
from yfinanceAPI import YahooAPI
import numpy as np

class Portfolio():
    stockList = []
    id = 0
    def __init__(self,id):
        self.id = id
        self.loadFromFile()

    def addStock(self,symbol,shares):
        self.stockList.append((symbol,shares))
        f = open("Portfolios/portfolio"+str(self.id)+".txt","a")
        f.write(str(symbol)+":"+str(shares)+"\n")
        f.close()

    def loadFromFile(self):
        if(self.id == 0):
            error("Invalid Portfolio Id")
            return
        f = open("Portfolios/portfolio"+str(self.id)+".txt", "r")
        for line in f:
            splitedList = line.split(":")
            if(len(splitedList) != 2):
                error("Portfolio File:"+str(self.id)+"wrong Format")
                return 
            self.stockList.append((splitedList[0],int(splitedList[1])))
        f.close()

    def removeStock(self,symbol):
        i = 0
        for stock in self.stockList:
            i = i +1
            if(stock[0][0] == symbol):
                break
        f = open("Portfolios/portfolio"+str(self.id)+".txt","r") 
    
    # Die Varianz-Kovarianz Matrix stellt in der diagonale die Varianz der Einzelwerte da
    # In den anderen Feldern stehen die Kovarianzen der jeweiligen Werte (WP1, Wp2), (WP1, WP3) etc
    # Mit Hilfe dieser Methode berechnen wir Opportunity Sets mit n > 2 Anlagen  

    # ToDo. StockList vom Portfolio anpassen für diese Methode
    def VarKovMatrix():
        stocks = ["MSFT","AAPL","BNTX"]
        data_stocks = []
        for symbol in stocks:
            data_stocks.append(YahooAPI.getOneYearYields(symbol))
        npArray = np.array(data_stocks)
        KovMatrix = np.cov(npArray, bias=True)
        print(KovMatrix)

    VarKovMatrix()
    
        