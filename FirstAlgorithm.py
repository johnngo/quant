###simple SPY Algorithms, we want to cut losses if spy loses 10% and take profits if SPY gains 10%, 
###after loss or gain is executes, stop for 1month before entering again
class MeasuredOrangeFish(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1) # Set Start Date
        self.SetEndDate(2021, 1, 1) # Set End Date
        self.SetCash(100000) # Set Strategy Cash

        spy = self.AddEquity("SPY", Resolution.Daily)
        #self.AddForex, self.AddFuture
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
        self.spy = spy.Symbol

        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time



    def OnData(self, data):
        if not self.spy in data:
            return 
        
        #price = data.Bars[self.spy].Close
        price = data[self.spy].Close
        #price = self.secruities[self.spy].close

        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.spy, 1)
                #self.MarketOrder(self.spy, int(self.Portfolio.Cash/ price) )
                self.Log("BUY SPY @" + str(price))
                self.entryPrice = price

        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.90 > price:
            self.Liquidate()
            self:Log("Sell SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period


