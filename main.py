import datetime
from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

contract = Stock('TSLA', 'SMART', 'USD')

dt = ''
barsList = []
i = 0
while True:
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=dt,
        durationStr='10 D',
        barSizeSetting='1 min',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1)
    if not bars or i == 10:
        break
    barsList.append(bars)
    dt = bars[0].date
    print(dt)
    i += 1

# save to CSV file
allBars = [b for bars in reversed(barsList) for b in bars]
df = util.df(allBars)
df.to_csv(contract.symbol + '.csv', index=False)