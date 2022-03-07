



from logging import error, raiseExceptions
from math import sqrt
from statistics import variance
from time import time


class Stock():
    symbol = ""
    last6Month = {}
    lastMonth = {}
    today = {}
    informations = {}
    lastYear = {}
    companyInfo = {}
    last5Years = {}
    yieldLast5Years = {}
    standartDeviation = 0
    averageYield = 0
    varianz = 0
    standartDevi = 0

    def __init__(self,symbol,informations,lastMonth,today,last6Month,lastYear, companyInfo,last5Years):
        self.symbol = symbol
        self.informations = informations
        self.lastMonth = lastMonth
        self.today = today
        self.last6Month = last6Month
        self.lastYear = lastYear
        self.companyInfo = companyInfo
        self.last5Years = last5Years
        self.yields = []
    def calc(self):

        self.yields = self.calcYields(60)
        self.averageYield = self.calcAverageYield(self.yields[1])
        self.varianz = self.calcVarianz()
        self.standartDevi = self.calcStandartDevi()

    def calcVarianz(self):
        if len(self.yields[1]) <= 0:
            error("No AverageYields")
        sum = 0
        for yields in self.yields[1]:
            sum = sum + (yields - self.averageYield)**2
        sum = sum / len(self.yields[1])
        return sum

    def calcStandartDevi(self):
        if(self.varianz <= 0):
            error("Varianz = 0")
        return sqrt(self.varianz)

    def calcYields(self,months):
        if(months < 12):
            error("calcYields: Less then 6 Months")
        years = int(months / 12)
        print("Years:")
        print(years)
        lastMonthIndex = len(self.last5Years["candles"]) - 1
        averageMonthlyYield = []
        averageYearlyYield = []
        for year in range(years):
            startMonthIndex = lastMonthIndex - year * 12
            endMonthIndex = startMonthIndex - 12
            averageMonthlyYieldForOneYear = self.calcMonthlyYieldAverage(startMonthIndex,endMonthIndex, self.last5Years["candles"])
            averageMonthlyYield.append(averageMonthlyYieldForOneYear)
            averageYearlyYield.append((1+averageMonthlyYieldForOneYear)**12-1)
            print(averageMonthlyYield)
        return [averageMonthlyYield,averageYearlyYield]

        

    def calcMonthlyYieldAverage(self, startIndex, endIndex, candleArray):
        if(startIndex < 0):
            error("calcMonthly: startIndex < 0")
        if(endIndex > startIndex or endIndex < 0):
            error("calcMonthly: endIndex wrong")
        monthlyYields = []
        print(endIndex)
        while (startIndex > endIndex and startIndex >0):
            print("StartIndex:")
            print(startIndex)
            yieldForOneMonth = (candleArray[startIndex]["close"] - candleArray[startIndex -1]["close"]) / candleArray[startIndex - 1]["close"]
            monthlyYields.append(yieldForOneMonth)
            startIndex = startIndex - 1 
        print("Monthly Yields")
        print (monthlyYields)
        return self.calcAverageYield(monthlyYields)


    def calcYieldMonthlytoYear(self):
        self.yieldLast5Years 



    def calcAverageYield(self, arrayOfYields):
        averageYield = 0
        for yields in arrayOfYields:
            averageYield = averageYield + yields
        averageYield = averageYield / len(arrayOfYields)
        return averageYield
