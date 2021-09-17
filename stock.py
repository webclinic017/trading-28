from _typeshed import Self


class Stock():
    def __init__(self) -> None:
        self.ticker : int = ""
        self.open : int = 0,
        self.high : int = 0,
        self.low : int = 0,
        self.close : int= 0,
        self.average : int = 0,
        self.volume : int = 0


class Position():
    def __init__(self) -> None:
        self.ticker : str = None
        self.size : float = 0
        self.buy_price : float = 0
        self.sell_price : float = 0
        self.pnl : float = 0
        

class Order():
    

    def __init__(self, ticker : str, op : int, type : str, price : int, size : int) -> None:
        '''
        
        op = 1 or 2 (1 = buy, 2 = sell)
        type = 'MTK' or 'LMT'
        '''
        self.ticker : str = ticker
        self.op : int = op
        self.type : str = type
        self.price : float = price 
        self.size : float = size

    def create_mkt_buy(ticker : str, size: float) -> Self:
        return Order(ticker, 1, 'MTK', size) 

    def create_mkt_sell(ticker : str, size : float) -> Self:
        return Order(ticker, 2, 'MTK', size)