import datetime
from typing import List, Tuple
import stock
import math
import bridge

class Strategy():
    def __init__(self, date: datetime, bridge: bridge.Bridge) -> None:
        self.positions : list[stock.Position] = None
        self.date = date
        self.bridge = bridge

    def actions(self) -> list:   
        '''
        return list of [orders]
        '''
        raise NotImplementedError


class SimpleMomentum(Strategy):
    # bridge is the method to get outside information
    def __init__(self, date: datetime, bridge: bridge.Bridge) -> None:
        super.__init__(date, bridge)


    def actions(self) -> list:
        # if first day of trading week
        if not self.bridge.is_trading_day(self.date - datetime.timedelta(days=1)):
            res = []
            budget = (self.bridge.cash * 0.1) / 10
            for s in self.check_buys():
                size = math.ceil(budget / self.bridge.get_stock(s).average)
                res.append(stock.Order.create_mkt_buy(s, size))
            
            return res

        # if last day of trading week
        elif not self.bridge.is_trading_day(self.date + datetime.timedelta(days=1)): 
            return self.sell_all()

        # else do nothing
        else:
            return []

    # TODO: move this to Strategy()
    def sell_all(self, buys = {}):
        actions = []
        for s in self.positions:
             actions.append(stock.Order.create_mkt_sell(s.ticker))

        return actions

    def check_buys(self) -> List[str]:

        open_date, close_date = self._find_last_trading_week()
        openday_vals: dict[str, stock.Stock] = self.bridge.get_all_stocks(open_date)
        closeday_vals: dict[str, stock.Stock] = self.bridge.get_all_stocks(close_date)

        # calculate % delta for all stocks
        pd = {}
        for s in self.bridge.all_tickers:
            pd[s] = self._calculate_prec_diff(openday_vals[s].open, closeday_vals[s].close)

        # sort for largest % delta
        pd = dict(sorted(pd.items(), key=lambda item: item[1], reverse=True))
        
        i = 0
        res = []
        for s in pd:
            if self.bridge.get_market_cap(s) > 500:
                res.append(s)
                i += 1

            if i == 10:
                break
        
        return res



    def sell_holdings(self):
        return self.holding_list


    def _calculate_prec_diff(week_open, week_close):
        return (week_close - week_open) / week_open


    def _find_last_trading_week(self) -> Tuple:
        pass