import tushare as ts
import time
print('Press Ctrl-C to stop')
try:
    while True:
        df = ts.get_realtime_quotes(['600030','600900'])
        df["TT"] = df["price"] - df["pre_close"]
        print(df[['TT','price','pre_close','open','high','low','volume','amount','time']])
        time.sleep(10)
except KeyboardInterrupt:
    print('\nDone.')