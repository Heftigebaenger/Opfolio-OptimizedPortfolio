from audioop import mul
from distutils.spawn import find_executable
from logging import error
from operator import truediv
from yfinanceAPI import YahooAPI
import numpy as np
import pandas as pd
from math import sqrt
from stock import Stock
import random
import matplotlib.pyplot as plt

class Portfolio():
    stockList = []
    id = 0
    def __init__(self,id):
        self.id = id
        #self.loadFromFile()

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
    def VarKovMatrix(self, stocks):
        data_stocks = pd.DataFrame()
        for symbol in stocks:
            data_stocks[symbol]=YahooAPI.getOneYearYields(symbol, lg=True)
        KovMatrix = data_stocks.cov()
        KovMatrix = KovMatrix.multiply(Stock.tradingdays)
        print(KovMatrix)
        return KovMatrix

    # ToDo: Ist aktuell noch nichts berechnet 
    def CorrMatrix(self,stocks):
        data_stocks = pd.DataFrame()
        for symbol in stocks:
            data_stocks[symbol]=YahooAPI.getOneYearYields(symbol, lg=True)
        CorrMatrix = data_stocks.corr()
        print(CorrMatrix)
        return CorrMatrix


    def multiPortfolio(self):
        stocks = ["MSFT","AAPL","BNTX","SAP"]
        yields = [0.2,0.6,0.3,0.4]
        #rndm_nr = np.empty()
        #port_shares = np.empty(0)
        #i = 0
        #while i < len(stocks):
         #   np.append(rndm_nr, random.random())
          #  i += 1
        #print(rndm_nr)


        randomMatrix = np.random.rand(500,len(stocks))
        sumRandomMatrix = np.sum(randomMatrix, axis=1)
        divisionMatix = np.tile(sumRandomMatrix, (len(stocks),1))
        anteilMatrix = randomMatrix / divisionMatix.T

        #yieldsBigMatrix = np.tile(yields, (500,1))
        #print("Yield Matrix")
        #print(yieldsBigMatrix.T)
        portfolioRenditeVector = np.dot(anteilMatrix,yields)
        
        varkovMatrix = np.array(self.VarKovMatrix(stocks))
        
        riskMatrix = np.apply_along_axis(self.multiPortfolioHelper,1,varkovMatrix,anteilMatrix).T
        riskMatrix = np.matmul(riskMatrix, anteilMatrix.T)
        riskVector = np.diagonal(riskMatrix)
        riskVector = np.sqrt(riskVector)
        print("riskVector")
        print(riskVector)
        print(portfolioRenditeVector)
        f = open("risk.txt","w")
        for i in riskVector:
            f.write(str(i)+"\n") 
        p = open("yield.txt","w")
        for i in portfolioRenditeVector: 
            p.write(str(i)+"\n")
        f.close()
        p.close()


    def multiPortfolioHelper(self,varkovMatrixVector,anteilMatrix):
        print(varkovMatrixVector)
        return np.dot(anteilMatrix,varkovMatrixVector)



portfolioOne = Portfolio(1)
portfolioOne.multiPortfolio()

  







    
        