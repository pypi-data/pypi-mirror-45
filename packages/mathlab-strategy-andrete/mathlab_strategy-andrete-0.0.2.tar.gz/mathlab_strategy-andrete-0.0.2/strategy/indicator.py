import talib
import numpy as np
import pandas as pd
from collections import deque
from decimal import Decimal


class Indicator():
    pass


def SMA(input_data, timeperiod=100):
    result = []
    q = deque(maxlen=timeperiod)
    for price in input_data:
        q.append(price)
        if len(q) < timeperiod:
            result.append(np.NAN)
        else:
            sma = sum([item for item in q]) / Decimal(timeperiod)
            result.append(sma)
    return pd.Series(result, index=input_data.index)

'''
close = np.random.random(100)
output = talib.SMA(close, 10)
print(output, type(output))
result = SMA(close, 10)
print(result)
'''

