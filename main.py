from datetime import datetime
from ib_insync import *
import models
import bridge

def main_loop(Strategy : models.Strategy):
    date : datetime = None 
    bg : bridge.Bridge = bridge.Bridge(None) # TODO:
    strategy : models.Strategy = Strategy(bg)

    while True:
        strategy.actions()
        strategy.execute_orders()
        bg.new_tick()
        


if __name__== "__main__":

    main_loop(None) # TODO: 