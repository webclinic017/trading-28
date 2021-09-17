from datetime import datetime
from ib_insync import *
import models
import bridge

def main_loop(strat : models.Strategy):
    date : datetime = None 
    bg : bridge.Bridge = bridge.Bridge(None) # TODO:
    strategy : models.Strategy = strat(date, bg)

    for date in bg:
        
        
        actions = strategy.actions()
        bg.execute_orders(actions)
        


if __name__== "__main__":

    main_loop(None) # TODO: 