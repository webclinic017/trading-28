class Stock():
    def __init__(self, ticker: str, open: float, high: float, low: float, close: float, average: float, volumn: float) -> None:
        self.ticker: str = ticker
        self.open: float = open
        self.high: float = high
        self.low: float = low
        self.close: float = close
        self.average: float = average
        self.volumn: float = volumn


class Position():
    def __init__(self, ticker: str) -> None:
        self.ticker: str = None
        self.size: float = 0
        self.buy_price: float = 0
        self.sell_price: float = None
        self.pnl: float = 0


    def buy(self,size, buy_price) -> float:
        self.buy_price = buy_price
        bought = buy_price * size
        self.size += size

        return bought

    def sell(self, size, sell_price) -> float:
        self.sell_price = sell_price
        spent = self.buy_price * size
        gained = self.buy_price *  size
        self.pnl += gained - spent
        self.size -= size

        return gained



class Order():

    def __init__(self, ticker: str, op: int, type: str, lmt_price: int, size: int) -> None:
        '''

        op = 1 or 2 (1 = buy, 2 = sell)
        type = 'MTK' or 'LMT'
        '''
        self.ticker: str = ticker
        self.op: int = op
        self.type: str = type
        self.lmt_price: float = lmt_price
        self.size: float = size

    def create_mkt_buy(ticker: str, size: float):
        return Order(ticker, 1, 'MTK', -1, size)

    def create_mkt_sell(ticker: str, size: float):
        return Order(ticker, 2, 'MTK', -1, size)
