import datetime
import csv
from os import write
import numpy
from ib_insync import *




if __name__== "__main__":

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)


    
    res = []

    with open('results.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)


        num = 0
        for row in reader:
            symbol = row["Symbol"]

            contract = Stock(symbol, 'SMART', 'USD')

            ticker = ib.reqMktData(contract, "258")
            ib.sleep(2) 


            try:
                if ticker.fundamentalRatios.MKTCAP > 500:
                    res.append(symbol)
                    num += 1

            except AttributeError:
                pass
            


            ib.cancelMktData(contract)

            if num > 10:
                break


    print(res)