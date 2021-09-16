import datetime
from typing import Tuple
import simulation

class Strategy():
    def __init__(self) -> None:
        pass

    def actions(self) -> list:   
        '''
        return [{dict of buy tickers and % of cash}, {dict of sell tickers and % of holding}]
        '''
        raise NotImplementedError


class SimpleMomentum(Strategy):
    # bridge is the method to get outside information
    def __init__(self, date: datetime, bridge: simulation.Bridge) -> None:
        self.holding_list = []
        self.date = date
        self.bridge = bridge


    def actions(self) -> list:
        
        res = [{}, {}]

        # if first day of trading week
        if not self.bridge.is_trading_day(self.date - datetime.timedelta(days=1)):
            buys = {}
            for s in self.check_buys():
                buys[s] = 0.1

            res.append(buys)
            res.append({})
        # if last day of trading week
        elif not self.bridge.is_trading_day(self.date + datetime.timedelta(days=1)): 
            res = self.sell_all()

        # else do nothing


        return res

    # TODO: move this to Strategy()
    def sell_all(self, buys = {}):
        sells = {}
        for s in self.holding_list:
            sells[s] = 1

        return [buys, sells]

    def check_buys(self):

        open_date, close_date = self._find_last_trading_week()
        openday_vals: dict[str, simulation.Stock] = self.bridge.get_all_stocks(open_date)
        closeday_vals: dict[str, simulation.Stock] = self.bridge.get_all_stocks(close_date)

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