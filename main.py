from datetime import datetime

### <summary>
### Simple indicator demonstration algorithm of MACD
### </summary>
class MACDTrendAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2017,01,05)  #Set Start Date
        self.SetEndDate(2018,01,04)    #Set End Date
        self.SetCash(100000)           #Set Strategy Cash

        self.SetBrokerageModel(BrokerageName.GDAX)
        self.AddCrypto("BTCUSD", Resolution.Daily)
        self.Securities["BTCUSD"].SetDataNormalizationMode(DataNormalizationMode.Raw);

        # define our daily macd(12,26) with a 9 day signal
        self.__macd = self.MACD("BTCUSD", 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
        self.__previous = datetime.min
        self.PlotIndicator("MACD", True, self.__macd, self.__macd.Signal)
        self.PlotIndicator("BTCUSD", self.__macd.Fast, self.__macd.Slow)


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # wait for our macd to fully initialize
        if not self.__macd.IsReady: return

        # only once per day
        if self.__previous.date() == self.Time.date(): return

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.006;

        holdings = self.Portfolio["BTCUSD"].Quantity

        signalDeltaPercent = (self.__macd.Current.Value - self.__macd.Signal.Current.Value)/self.__macd.Fast.Current.Value

        # if our macd is greater than our signal, then let's go long
        if holdings <= 0 and signalDeltaPercent > tolerance:  # 0.01%
            # longterm says buy as well
            self.SetHoldings("BTCUSD", 1.0)

        # of our macd is less than our signal, then let's go short
        elif holdings >= 0 and signalDeltaPercent < -tolerance:
            self.Liquidate("BTCUSD")


        self.__previous = self.Time
