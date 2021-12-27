class Stock():
    symbol = ""
    lastMonth = {}
    today = {}
    informations = {}

    def __init__(self,symbol,informations,lastMonth,today):
        self.symbol = symbol
        self.informations = informations
        self.lastMonth = lastMonth
        self.today = today

