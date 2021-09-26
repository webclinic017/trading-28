import datetime
from typing import List, Sized
import ib_insync
import stock
import source
import csv



class Bridge():
    def __init__(self) -> None:
        self.curtime = None
        self.all_tickers = []
        self.cash = 1000000 # TODO: make it not hard coded
        self.source = source
        self.holdings = {}

        # ib
        self.ib = ib_insync.IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)


    def is_trading_day(self, date: datetime.datetime) -> bool:
        raise NotImplementedError

    def get_all_stocks(self) -> dict:
        '''
        {ticker : Stock}
        '''
        raise NotImplementedError

    def get_stock(self, ticker: str) -> stock.Stock:
        raise NotImplementedError

    def get_market_cap(self, ticker: str) -> float:
        contract = ib_insync.Stock(ticker, 'SMART', 'USD')

        s = self.ib.reqMktData(contract, "258")
        self.ib.sleep(2) 
        return s.fundamentalRatios.MKTCAP

    def execute_orders(self, actions : List[stock.Order]):
        raise NotImplementedError

    def new_tick(self):
        '''
        blocking
        '''
        self.collect_info()
        

    def collect_info(self) -> None:
        raise NotImplementedError


    def net_worth(self) -> float:
        raise NotImplementedError

    def last_trading_tick(self) -> datetime:
        raise NotImplementedError


class Simulation(Bridge):
    def __init__(self) -> None:
        super().__init__()
        history_csv = "history.csv"
        self.data = {}
        print("Simulation: start")
        self._read_csv(history_csv)
        self.pending_orders: list[stock.Order] = []

    def _read_csv(self, history_csv):
        print("Simulation: reading history")
        with open(history_csv) as f:
            reader = csv.DictReader(f)
            for row in reader:

                temp = {}

                if row["date"] == '':
                    continue

                for k, v in row.items():
                    # skip date and empty stocks
                    if k == "date":
                        continue
                    elif v == '':
                        continue

                    vals = v.split("|")
                    temp[k] = stock.Stock(k, vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])



                self.data[datetime.datetime.strptime(row["date"], "%Y/%m/%d")] = temp
        
        # set curtime to the start time + 10 days
        self.curtime = list(self.data.keys())[0] + datetime.timedelta(days=10)
                
    def is_trading_day(self, date: datetime.datetime = None) -> bool:

        if date is None:
            date = self.curtime

        return date in self.data

    def get_all_stocks(self) -> dict:
        ''' 
        {ticker : Stock}
        '''
        return self.data[self.last_trading_tick()]


    def get_stock(self, ticker: str) -> stock.Stock:
        return self.data[self.curtime][ticker]


    def execute_orders(self, actions : List[stock.Order]):
        self.pending_orders += actions  

    def collect_info(self) -> None:
        print("Simulation: Day " + str(self.curtime)) 
        # advance time
        self.curtime += datetime.timedelta(days=1)

        # execute orders
        if (self.is_trading_day()):
            for order in self.pending_orders:
                if order.op == 1:
                    if order.type == 'MTK':
                        s = self.get_stock(order.ticker)
                        buying = stock.Position(order.ticker)
                        spent = buying.buy(order.size, s.open)
                        self.holdings[s.ticker] = buying
                        self.pending_orders.remove(order)
                        self.cash -= spent

                elif order.op == 2:
                    if order.type == 'MTK':
                        s = self.get_stock(order.ticker)
                        gained = self.holdings[s.ticker].sell(order.size, s.open)
                        self.pending_orders.remove(order)
                        self.cash += gained

        print(self.net_worth())
        
        # stop simulation
        if (self.curtime == list(self.data.keys())[-1]):
            print("Simulatuon: exixiting at " + str(self.curtime))
            exit()
                    
    def net_worth(self) -> float:
        res = self.cash
        for k, v in self.holdings:
            res += v.size * self.get_stock(v.ticker).close

        return res

    def last_trading_tick(self) -> datetime:
        day = self.curtime
        i = 0
        while True:
            if self.is_trading_day(day):
                return day
            else:
                day -=  datetime.timedelta(days=1)

            i += 1

            if i == 30:
                raise IndexError("Something is very wrong with the stock market")
