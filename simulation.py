from datetime import datetime

class Stock():
    def __init__(self) -> None:
        self.ticker = ""
        self.open = ""
        self.close = ""

class Bridge():
    def __init__(self) -> None:
        self.curtime = None
        self.all_tickers = []
        pass

    def is_trading_day(self, date: datetime) -> bool:
        pass

    def get_all_stocks(self, date: datetime = None) -> dict:
        '''
        {ticker : Stock}
        '''
        pass

    def get_market_cap(self, ticker: str) -> float:
        pass

class Simulation():
    def __init__(self) -> None:
        pass


    def main_loop(self):
        pass