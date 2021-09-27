import datetime
from typing import List, Tuple
import stock
import math
import bridge

class Strategy():
    def __init__(self, bridge: bridge.Bridge) -> None:
        self.bridge = bridge
        self.orders = []

    def actions(self) -> None:   
        '''
        return list of [orders]
        '''
        self.orders = self._actions()

    def _actions(self) -> list:
        raise NotImplementedError

    def execute_orders(self) -> None:
        self.bridge.execute_orders(self.orders)
        # reset orders list
        self.orders = []


class SimpleMomentum(Strategy):
    # bridge is the method to get outside information
    def __init__(self, bridge: bridge.Bridge) -> None:
        super().__init__(bridge)



    def _actions(self) -> list:
        # the tick after friday close
        if not self.bridge.is_trading_day(self.bridge.curtime) and self.bridge.is_trading_day(self.bridge.curtime - datetime.timedelta(days=1)):
            print("SMM: searhing for new stocks")
            res = []
            budget = (self.bridge.cash * 0.1) / 10
            for s in self.check_buys():
                st = self.bridge.get_stock(s)
                if st:
                    size = math.ceil(budget / st.open)
                    res.append(stock.Order.create_mkt_buy(s, size))

            print("SMM: buying " + ','.join([s.ticker for s in res]))
            return res

        # if last day of trading week
        elif not self.bridge.is_trading_day(self.bridge.curtime + datetime.timedelta(days=1)): 
            print("SMM: selling all")
            return self.sell_all()

        # else do nothing
        else:
            return []

    # TODO: move this to Strategy()
    def sell_all(self, buys = {}):
        actions = []
        for k, v in self.bridge.holdings.items():
             actions.append(stock.Order.create_mkt_sell(k, v.size))

        return actions

    def check_buys(self) -> List[str]:

        open_date, close_date = self._find_last_trading_week()
        openday_vals: dict[str, stock.Stock] = self.bridge.get_all_stocks(open_date)
        closeday_vals: dict[str, stock.Stock] = self.bridge.get_all_stocks(close_date)

        # calculate % delta for all stocks
        pd = {}
        for s in self.bridge.all_tickers:
            try: 
                pd[s] = self._calculate_prec_diff(openday_vals[s].open, closeday_vals[s].close)
            except KeyError:
                continue

        # sort for largest % delta
        pd = dict(sorted(pd.items(), key=lambda item: item[1], reverse=True))
        
        i = 0
        res = []
        for s in pd:
            #if self.bridge.get_market_cap(s) > 500:
            res.append(s)
            i += 1

            if i == 10:
                break
        
        return res



    def sell_holdings(self):
        return self.holding_list


    def _calculate_prec_diff(self, week_open, week_close):
        return (week_close - week_open) / week_open


    def _find_last_trading_week(self) -> Tuple:
       i = 0
       flag = 1
       day = self.bridge.curtime

       while True:          
            # for the last day, we are going from holiday to the trading day
            if flag == 1:
                if self.bridge.is_trading_day(day):
                    last_day = day
                    flag = 2
            # for the first day, we are going from trading day to the last holiday
            elif flag == 2:
                if not self.bridge.is_trading_day(day):
                    first_day = day + datetime.timedelta(days=1)
                    return (first_day, last_day)



            if i == 30:
                raise IndexError("Something is very wrong with the stock market")

            i += 1
            day -= datetime.timedelta(days=1)

