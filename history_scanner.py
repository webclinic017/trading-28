import datetime
import csv
from ib_insync import *

import sys

import ib_insync

# https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  

if __name__== "__main__":

    ib = ib_insync.IB()
    ib.connect('127.0.0.1', 7497, clientId=1)


    res = {}
    header = ["date"]
    # read count
    i = 0
    # false ones
    f = 0
        

    with open('all_symbols.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)

        total_row = sum(1 for row in reader)

        csvfile.seek(0)

        for row in reader:
            symbol = row["Symbol"]
            

            contract = ib_insync.Stock(symbol, 'SMART', 'USD', primaryExchange='NASDAQ')

            bars = ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='5 Y',
                barSizeSetting='1 day',
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1)

            # if data pulled correctly
            try:
                j = bars[0]
            except IndexError:
                f += 1
                continue

            header.append(symbol)

            for d in bars:
                # open | high | low | close | average | volume 
                data = "{0}|{1}|{2}|{3}|{4}|{5}".format(
                    d.open,
                    d.high,
                    d.low,
                    d.close,
                    d.average,
                    d.volume
                )

                date = d.date.isoformat()

                if date not in res.keys():
                    res[date] = {}

                res[date][symbol] = data

            i += 1

            progress(i, total_row, str(i) + "/" + str(total_row))
            # if (i == 10):
            #    break

    
    print("Total " + str(total_row) + " scanned and " + str(total_row - f) + " successes")
            
    # save to CSV file
    with open('history.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for k, v in res.items():
            
            line = v
            line["date"] = k

            writer.writerow(line)

    
