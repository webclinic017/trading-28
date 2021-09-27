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

        self.mktcap_cache = {}

        # ib
        self.ib = ib_insync.IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)


    def is_trading_day(self, date: datetime.datetime) -> bool:
        raise NotImplementedError

    def get_all_stocks(self, date: datetime.datetime) -> dict:
        '''
        {ticker : Stock}
        '''
        raise NotImplementedError

    def get_stock(self, ticker: str, date: datetime.datetime) -> stock.Stock:
        raise NotImplementedError

    def get_market_cap(self, ticker: str) -> float:
        

        if ticker in self.mktcap_cache:
            return self.mktcap_cache[ticker]


        contract = ib_insync.Stock(ticker, 'SMART', 'USD', primaryExchange='NASDAQ')
        s = self.ib.reqMktData(contract, "258")
        self.ib.sleep(2) # TODO: find a way to optimize this

        try:
            res = s.fundamentalRatios.MKTCAP
        except:
            res = 0

        self.ib.cancelMktData(contract)
        self.mktcap_cache[ticker] = res
        return res

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
        history_csv = "data/history.csv"
        self.data = {}
        print("Simulation: start")
        self._read_csv(history_csv)
        self.pending_orders: list[stock.Order] = []

        self._pref_file = open("pref.csv", "w")
        self._writer = csv.writer(self._pref_file)
   

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
                    temp[k] = stock.Stock(k, float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3]), float(vals[4]), float(vals[5]))
                    self.all_tickers.append(k)



                self.data[datetime.datetime.strptime(row["date"], "%Y/%m/%d")] = temp
        
        # set curtime to the start time + 10 days
        self.curtime = list(self.data.keys())[0] + datetime.timedelta(days=10)
        self.all_tickers = list(set(self.all_tickers))
                
    def is_trading_day(self, date: datetime.datetime = None) -> bool:

        if date is None:
            date = self.curtime
        
        for k in self.data.keys():
            if k == date:
                return True

        return False

    def get_all_stocks(self, date: datetime.datetime = None) -> dict:
        ''' 
        {ticker : Stock}
        '''

        if not date:
            date = self.last_trading_tick()

        return self.data[date]


    def get_stock(self, ticker: str, date: datetime.datetime = None) -> stock.Stock:
        if not date:
            date = self.last_trading_tick()

        try:
            return self.data[date][ticker]
        except KeyError:
            return None


    def execute_orders(self, actions : List[stock.Order]):
        self.pending_orders += actions  

    def collect_info(self) -> None:
        print("Simulation: Day " + str(self.curtime)) 
        # advance time
        self.curtime += datetime.timedelta(days=1)

        # execute orders
        if (self.is_trading_day()):
            for order in self.pending_orders:
                
                if not self.get_stock(order.ticker):
                    self.pending_orders.remove(order)
                    continue

                if order.op == 1:
                    if order.type == 'MTK':
                        s = self.get_stock(order.ticker)
                        buying = stock.Position(order.ticker)
                        spent = buying.buy(order.size, s.open)
                        self.holdings[s.ticker] = buying
                        self.pending_orders.remove(order)

                        # do not use margin too much
                        # TODO: make this variable
                        if (self.cash - spent < self.net_worth() * -0.1):
                            continue

                        self.cash -= spent

                elif order.op == 2:
                    if order.type == 'MTK':
                        s = self.get_stock(order.ticker)
                        gained = self.holdings[s.ticker].sell(order.size, s.open)
                        self.pending_orders.remove(order)
                        self.cash += gained
        
        # stop simulation
        if (self.curtime == list(self.data.keys())[-1]):
            print("Simulation: ends at " + str(self.curtime))
            self._pref_file.close()
            exit()

        print("Simulation: networth " + str(self.net_worth()))
        self._writer.writerow([str(self.curtime), str(self.net_worth())])
        self._pref_file.flush()
                    
    def net_worth(self) -> float:
        res = self.cash
        for k, v in self.holdings.items():
            stk = self.get_stock(k)
            if stk:
                res += v.size * stk.close

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
