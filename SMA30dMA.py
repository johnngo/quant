#identify uptrend or downtrend, trading spy, sma, price above sma, uptrend, else downtrend, how close is it to 52 weeks highs
# go long, low 52 week highs, sell. 

class CalculatingFlourescentOrangeCamel(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.sma = self.SMA(self.spy, 30, Resolution.Daily)
        closing_prices = self.History(self.spy, 30, Resolution.Daily)["close"]
        for time, price in closing_prices.loc[self.spy].items():
            self.sma.Update(time, price)

    def OnData(self, data):
        if not self.sma.IsReady:
            return

        hist = self.History(self.spy, timedelta(365), Resolution.Daily)
        low = min(hist["low"])
        high = max(hist["high"])

        price = self.Securities[self.spy].Price
        
        if price * 1.05 >= high and self.sma.Current.Value < price:
            if not self.Portfolio[self.spy].IsLong:
                self.SetHoldings(self.spy, 1)

        elif price * 0.95 <= low and self.sma.Current.Value > price:
            if not self.Portfolio[self.spy].IsShort:
                self.SetHoldings(self.spy, -1)

        else:
            self.Liquidate()

        self.Plot("Benchmark", "52w-High", high)
        self.Plot("Benchmark", "52w-High", low)
        self.Plot("Benchmark", "SMA", self.sma.Current.Value)


