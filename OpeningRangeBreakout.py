##opening range breakout

##breakout uses a defined period of time to set a price-range
##and trades on leaving that range.
##To achieve this we will start by consolidating the first
##30 minutes of data

class OpenRangeBreakout(QCAlgorithm):

    openingBar = None
    currentBar = None

    def Initialize(self):
        self.SetStartDate(2018, 7 , 10)
        self.SetEndDate(2019, 6 , 30)
        self.SetCash(100000)

        #subscribe to TSLA with minute resolution
        self.symbol =self.AddEquity("TSLA", Resolution.Minute)
        self.Consolidate("TSLA", timedelta(mintues =30), self.OnDataConsolidated)

        self.Scheduel.On(self.DateRules.EveryDay("TSLA"), self.TimeRules.At(13,30), self.ClosePositions)

    def OnData(self, data):
        
        #1 if self.Portfolio.Invested is true, or if the openingBar is None, return
        if self.Portfolio.Invested or self.openingBar is None:
            return
        #2 Check if the close price is above the high price, if so go 100% long on Tsla
        if self.Securities["TSLA"].Close > self.openingBar.High:
            self.SetHoldings("TSLA", 1)

        #3 Check if the close price is below the low price, if so go 100 short on TSLA
        if self.Securities["TSLA"].Close < self.openingBar.Low:
            self.SetHolindgs("TSLA", -1)

    #create a function OnDataConsolidator which saves the currentBar as basr
    def OnDataConsolidated(self, bar):
        if bar.Time.hour == 9 and bar.Time.minute == 30:
            self.openingBar = bar

    def ClosePositions(self):

        self.openingBar = None
        self.Liquidate("TSLA")


