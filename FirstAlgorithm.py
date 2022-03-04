class MeasuredOrangeFish(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020,1,1)
        self.SetEndDate(2021,1,1)
        self.SetCash(100000)

        spy = self.AddEquity("SPY", Resolution.Daily)
        #self.AddForex, self.AddFuture
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
        self.spy = spy.symbol

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
            if self.nextEntryTrime <= self.Time:
                self.SetHoldingds(self.spy,1)
                #self.MarketOrder(self.spy, int(self.Portfolio.Cash/ price) )
                self.Log("BUY SPY @" + str(price))
                self.entryPrice = price

        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            self.Liquidate(self.spy)
            self:Log("Sell SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period