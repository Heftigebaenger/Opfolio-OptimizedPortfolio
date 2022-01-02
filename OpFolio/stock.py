class Stock():
    symbol = ""
    last6Month = {}
    lastMonth = {}
    today = {}
    informations = {}

    def __init__(self,symbol,informations,lastMonth,today,last6Month):
        self.symbol = symbol
        self.informations = informations
        self.lastMonth = lastMonth
        self.today = today
        self.last6Month = last6Month

