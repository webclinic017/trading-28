from datetime import datetime
from ib_insync import *
import models
import bridge
import time


def main_loop(Bridge: bridge.Bridge, Strategy : models.Strategy):
    bg : bridge.Bridge = Bridge()
    strategy : models.Strategy = Strategy(bg)

    while True:
        strategy.actions()
        strategy.execute_orders()
        bg.new_tick()        


if __name__== "__main__":

    bg = bridge.Simulation
    strategy = models.SimpleMomentum

    print("Begin")
    main_loop(bg, strategy) 