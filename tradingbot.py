# lumibot: algo trading framework
# alpaca-trade-api-python: scrapes for news and places trades to broker
# torch: pytorch framework for using AI
# transformers: load up finance deep learning model

import math
from lumibot.brokers import Alpaca # broker
from lumibot.backtesting import YahooDataBacktesting # framework for testing
from lumibot.strategies.strategy import Strategy # trading bot
from lumibot.traders import Trader # deployment capability
from datetime import datetime, timedelta # helps to calculate up time
# from alpaca_trade_api import REST # used to give news to ML

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
    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol # Index of traded stock
        self.sleeptime = "24H" # Frequency of trades
        self.last_trade = None # Last trade
        self.cash_at_risk = cash_at_risk # Percent of cash at risk
        # self.api = REST(base_url=BASE_URL, # Create instance of trade api
        #                 key_id=API_KEY, 
        #                 secret_key=API_SECRET)

    # Amount of cash that will be invested
    def position_sizing(self):
        cash = self.get_cash() # Amount of cash in account
        last_price = self.get_last_price(self.symbol)

        if last_price != 0:
            quantity = math.floor(cash * self.cash_at_risk / last_price) # Amount of cash at risk
        return cash, last_price, quantity
    
    # def get_news(self):
    #     today, three_days_prior = self.get_dates()
    #     news = self.api.get_news(symbol=self.symbol,
    #                             start=three_days_prior, 
    #                             end=today)
    #     news = [ev.__dict__["_raw"]["headline"] for ev in news]
    #     return news

    # def get_dates(self):
    #     today = self.get_datetime()
    #     three_days_prior = today - timedelta(days=3)
    #     return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    # Runs everytime new data is received (trading logic)
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        if cash > last_price: # Check that there is enough cash in account to make purchase
            if self.last_trade == None:
                # news = self.get_news
                # print(news)
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price = last_price * 1.2, # Sell any profit when up 20%
                    stop_loss_limit_price = last_price * 0.95 # Sell any losses when down 5%
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
                    parameters={"symbol":"SPY",
                                "cash_at_risk":0.5}) 

# Instatiate back tester
strategy.backtest(YahooDataBacktesting,
                  start_date, 
                  end_date, 
                  parameters={"symbol":"SPY",
                              "cash_at_risk":0.5})
