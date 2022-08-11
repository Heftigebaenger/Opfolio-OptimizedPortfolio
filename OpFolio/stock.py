



from calendar import prmonth
from logging import error, raiseExceptions
from math import sqrt
from statistics import variance
from time import time
from datetime import datetime
from typing import Final, final
import numpy as np


#Schreibe getDay methode


# Stock Class to uniform Stockdata
class Stock():
    """Cointains all information for a single stock as well as calculation with the stock informations

    Attributes: 
        symbol (str): Unique symbol to identify stock
        informations (dictionary): Containts information about the stock
        conpanyInfo (dictionary): Contains information about the stock company

        today (dictionary): Contains candles for every 5 minutes for today
        lastMonth (dictionary): Contains candels for each day for the last month
        last6Month (dictionary): Contains candles for each day for the last six month
        lastYear (dictionary): Contains candles for each week for the last year
        last5Years (dictionary): Contains candles for each month for the last five years
        last5YearsDaily (dictionary): Contains candles for each day for the last five years

    Methods:
        calc()  
            Calculates yields, varianz and deviation for the stock
        
        calcDailyYields(start,end)
            Returns an array with all daily yields between the start date and end date. 
            Start and end are based on the last5YearsDaily array

        yieldForTwoDays(dateOne,dateTwo)
            Returns the logarithic yield between two given dates

        printCandleData(index):
            prints the price and date for one candle data. 
            The given index is used to find the data in the last5YearsDaily array.

        calcVarianz(start,end,average)
    """

    tradingdays: Final = 250
    #Basic Information
    symbol = ""
    informations = {}
    companyInfo = {}
    
    #Stock price data
    today = {}
    lastMonth = {}
    last6Month = {}
    lastYear = {}
    last5Years = {}
    last5YearsDaily = {}

    #Calculated Data
    dailyYieldAverageYearOne = 0
    averageYield = 0
    varianzOneYear = 0
    standartDeviOneYear = 0
    yieldMonthly = []
    yieldForEachYear = []
    yieldLast5Years = 0
    last5YearsDailyYields = []

    def __init__(self,symbol,informations,lastMonth,today,last6Month,lastYear,companyInfo,last5Years,last5YearsDaily):
        self.symbol = symbol
        self.informations = informations
        self.lastMonth = lastMonth
        self.today = today
        self.last6Month = last6Month
        self.lastYear = lastYear
        self.companyInfo = companyInfo
        self.last5Years = last5Years
        self.yieldForEachYear = [0,0,0,0,0]
        self.yields = []
        self.yieldMonthly = []
        self.last5YearsDaily = last5YearsDaily
        self.last5YearsDailyYields = []

    def calc(self):
        self.yieldLast5Years = self.yieldForTwoDays(0,self.tradingdays*5)
        print(".........................")
        for i in range(5):
            self.yieldForEachYear[i] = self.yieldForTwoDays(self.tradingdays*i,self.tradingdays*(i+1))
        print(".........................")
        self.averageYield = self.calcAverageYield(self.yieldForEachYear)
        self.last5YearsDailyYields = self.calcDailyYields(0,5* self.tradingdays)
        self.dailyYieldAverageOneYear = self.calcAverageYield(self.last5YearsDailyYields[0:self.tradingdays])
        self.varianzOneYear = self.calcVarianz(0,self.tradingdays,self.dailyYieldAverageOneYear)
        self.standartDeviOneYear = self.calcStandartDevi(self.varianzOneYear)


    def calcDailyYields(self,start,end):
        dailyYields = []
        if(start > end or start < 0):
            error("Start is not Valid")
        if(end > len(self.last5YearsDaily["candles"])):
            end = len(self.last5YearsDaily["candles"]) -1
        for i in range(start,end):
           dailyYields.append(self.yieldForTwoDays(i,i+1))
        return dailyYields
     
    # Calculates the yield for two given Days  
    # 0 = Today,  365 = One Year ago
    # Yields calculated with ln(e) to include compound interest
    def yieldForTwoDays(self,dateOne, dateTwo):
        oldDate = 0
        newDate = 0
        #Check which date comes first
        if(dateOne < dateTwo): 
            oldDate = dateTwo
            newDate = dateOne
        else:
            oldDate = dateOne
            newDate = dateTwo
        if(oldDate > len(self.last5YearsDaily["candles"])):
            oldDate = len(self.last5YearsDaily["candles"])-1
 
        oldDate = len(self.last5YearsDaily["candles"]) - oldDate -1 
        newDate = len(self.last5YearsDaily["candles"]) - newDate -1 
        self.printCandleData(oldDate)
        self.printCandleData(newDate)
        print(np.log(self.last5YearsDaily["candles"][newDate]["close"] / self.last5YearsDaily["candles"][oldDate]["close"]))
        return np.log(self.last5YearsDaily["candles"][newDate]["close"] / self.last5YearsDaily["candles"][oldDate]["close"])
        #return (self.last5YearsDaily["candles"][newDate]["close"] - self.last5YearsDaily["candles"][oldDate]["close"]) / self.last5YearsDaily["candles"][oldDate]["close"]


    def printCandleData(self,index):
        date = self.last5YearsDaily["candles"][index]["datetime"]
        price = str(self.last5YearsDaily["candles"][index]["close"])
        date = datetime.fromtimestamp(date/1000)
        print("Price:"+price+"Date:"+ datetime.strftime(date,"%Y-%m-%d"));


    def calcVarianz(self,start,end,average):
        if(start > end or start < 0):
            error("Start is not Valid")
        if(end > len(self.last5YearsDaily["candles"])):
            end = len(self.last5YearsDaily["candles"]) - 1
        sum = 0
        for i in range(start,end):
            sum = sum + (self.last5YearsDailyYields[i] - average)**2
           #print(sum)
        sum = sum
        return sum

    def calcStandartDevi(self,varianz):
        if(varianz <= 0):
            error("Varianz = 0")
        return sqrt(varianz)


    def calcAverageYield(self,arrayOfYields):
        averageYield = 0
        for yields in arrayOfYields:
            averageYield = averageYield + yields
        averageYield = averageYield / len(arrayOfYields)
        print("Length of Avrage Array: "+str(len(arrayOfYields)))
        return averageYield

    def getCloseOfIndex(self,index):
        index = len(self.last5YearsDaily["candles"]) - index -1
        if(index < 0):
            error("Index to high")
        return self.last5YearsDaily["candles"][index]["close"]

    #Schreibe getDay methode
    @staticmethod
    def calcCorrelationCoefficient(stockA,stockB):

        years = 1
        #Zaehler
        zaehler = 0
        summx = 0
        summxx = 0
        xy = 0
        summy = 0
        summyy = 0
        
        for n in range(stockA.tradingdays):
            xy = xy + stockA.getCloseOfIndex(n)*stockB.getCloseOfIndex(n)

        for n in range(stockA.tradingdays):
            summx = summx + stockA.getCloseOfIndex(n)
            summxx = summxx + stockA.getCloseOfIndex(n)**2

        for n in range(stockA.tradingdays):
            summy = summy + stockB.getCloseOfIndex(n)
            summyy = summyy + stockB.getCloseOfIndex(n)**2
        zaehler = stockA.tradingdays * xy - summx * summy
        print("N ="+ str(stockA.tradingdays))
        print("Sum xy =" + str(xy))
        print("Sum x =" + str(summx))
        print("Sum y =" + str(summy))
        print("Zaehler =" + str(zaehler))

        #Nenner

        varianzx = stockA.tradingdays * summxx - summx**2   
        varianzy = stockA.tradingdays * summyy - summy**2
        varxy = varianzx* varianzy
        nenner = sqrt(varxy)
        

        corr = zaehler/nenner
        print("Varianzx =" + str(varianzx))
        print("Varianzy = " + str(varianzy))
        print("Varxy =" + str(varxy))
        print("Nenner =" + str(nenner))
        print(corr)
        return corr

