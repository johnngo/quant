## Setting up Momentum Based Tactical Allocation 

class MomentumBasedTacticalAllocation(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 8, 1) #Set Start Date
        self.SetEndDate(2021, 1, 1) # Set End Date
        self.SetCash(3000)
        #1 Subscribe to SPY -- S&P 500 Index ETF .. using daily resolution
        self.AddEquity("SPY", Resolution.Daily)
        self.AddEquity("BND", Resolution.Daily)
        #2 Subscribe to BND -- Vangaurd Total Bond Market ETF .. using daily resolution
        self.spyMomentum = self.MOMP("SPY", 50, Resolution.Daily)

        self.bondMomentum = self.MOMP("BND", 50, Resolution.Daily)

        #1 set SPY Benchmark
        self.SetBenchmark("SPY")

        #2 warm up algorithm for 50 days to populate the indicators prior to the start date
        self.SetWarmUp(50)



    def onData(self, data):
        #if self.spyMomentum is None or self.bondMomentum is None or not self.bondMomentum.IsReady or not self.spyMomentum.IsReady:
        if self.IsWarmingUp:
            return
        
        if self.spyMomentum.Current.Value > self.bondMomentum.Current.Value:
            self.liquidate("BND")
            self.SetHoldings("SPY", 1)

        #2 Otherwise we liquidate our holdings in SPY and allocate 100% to BND
        else:
            self.liquidate("SPY")
            self.SetHoldings("BND", 1)

        