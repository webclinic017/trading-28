import datetime
import csv
from os import write
import numpy
from ib_insync import *



def calculate_prec_diff(data1: BarData, data2: BarData):
    return (data2.close - data1.open) / data1.open


if __name__== "__main__":

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)



    with open('all_symbols.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)

        res = {}
        # total tickers
        t = 0
        # false ones
        f = 0
        
        for row in reader:
            symbol = row["Symbol"]

            contract = Stock(symbol, 'SMART', 'USD')

            bars = ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='5 D',
                barSizeSetting='1 day',
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1)

    
            if len(bars) != 5:
                f += 1
                continue

            pd = calculate_prec_diff(bars[0], bars[-1])
            res[symbol] = pd
            t += 1


            

        pd = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))

    print("Total " + str(t) + " scanned and " + str(t - f) + " successes")


    
    with open('results.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
        writer = csv.DictWriter(f, ["Symbol", "prec change"])
        writer.writeheader()
        for row in pd.items():
            writer.writerow({"Symbol":row[0], "prec change":row[1]})