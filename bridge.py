from datetime import datetime
from typing import List
import stock
import source

class Bridge():
    def __init__(self, source) -> None:
        self.curtime = None
        self.all_tickers = []
        self.cash = 0
        self.source = source
        pass




    def is_trading_day(self, date: datetime) -> bool:
        pass

    def get_all_stocks(self, date: datetime = None) -> dict:
        '''
        {ticker : Stock}
        '''
        pass

    def get_stock(self, ticker: str) -> stock.Stock:
        pass

    def get_market_cap(self, ticker: str) -> float:
        pass

    def execute_orders(self, actions : List[stock.Order]):
        pass

    def __next__(self):
        self.collect_info()

    def collect_info(self):
        raise StopIteration
        