class MeasuredOrangeFish(QCalgorithm):

    def Initialize(self):
        self.SetStartDate(2020,1,1)
        self.SetEndDate(2021,1,1)
        self.SetCash(100000)

        spy = self.AddEquity("SPY", Resolution.Daily)
        