from datetime import datetime
from ib_insync import *
import models
import bridge

def main_loop(Strategy : models.Strategy):
    date : datetime = None 
    bg : bridge.Bridge = bridge.Simulation() # TODO:
    strategy : models.Strategy = models.SimpleMomentum(bg)

    while True:
        strategy.actions()
        strategy.execute_orders()
        bg.new_tick()        


if __name__== "__main__":
    print("Begin")
    main_loop(None) # TODO: 