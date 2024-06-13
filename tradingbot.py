# lumibot: algo trading framework
# alpaca-trade-api-python: scrapes for news and places trades to broker
# torch: pytorch framework for using AI
# transformers: load up finance deep learning model

import os
from lumibot.brokers import Alpaca # broker
from lumibot.backtesting import YahooDataBacktesting # framework for testing
from lumibot.strategies.strategy import Strategy # trading bot
from lumibot.traders import Trader # deployment capability
from datetime import datetime 

# Credentials to Alpaca account
API_KEY = "PK6AZHT8T4HQ44PAVRAE"
API_SECRET = "hNxmBZZ7TxChsZl5RZrm2Sdwa2rm7yHhxTVBdY8T"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

# Holds all trading logic
class MLTrader(Strategy):
    # Initialized once at beginning (setup logic)
    def initialize(self, symbol:str="SPY"):
        self.symbol = symbol # Index of traded stock
        self.sleeptime = "24H" # Frequency of trades
        self.last_trade = None # Last trade

    # Runs everytime new data is received (trading logic)
    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )
            self.submit_order(order)
            self.last_trade = "buy"

# Initialize start and end dates
start_date = datetime(2024, 4, 20)
end_date = datetime(2024, 5, 20)

# Instantiate broker
broker = Alpaca(ALPACA_CREDS)

# Instatiate trader
strategy = MLTrader(name='mlstrat',
                    broker=broker, 
                    parameters={"symbol":"SPY"}) 

# Instatiate back tester
strategy.backtest(YahooDataBacktesting,
                  start_date, 
                  end_date, 
                  parameters={"symbol":"SPY"})
