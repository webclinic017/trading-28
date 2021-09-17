from datetime import datetime
import stock


class Bridge():
    def __init__(self) -> None:
        self.curtime = None
        self.all_tickers = []
        self.cash = 0
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

class Simulation():
    def __init__(self) -> None:
        pass


    def main_loop(self):
        pass