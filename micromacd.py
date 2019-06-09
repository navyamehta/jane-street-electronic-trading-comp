#We implement an innovative "micro" version of the Moving Average Convergence Divergence (MACD) Indicator by using
#12-reading and 20-reading exponential moving averages from the live inputs from the market-place. We have a small
#error margin of 0.15 to ensure that minor fluctuations don't severely affect our positions.

import pandas as pd
import numpy as np

avgprc = np.array([])
reading12ema = np.zeros(11)
reading20ema = np.zeros(19)

def micromacd (sellprc, buyprc, curhold):
    avgprc = np.insert(avgprc, 0, sum([sellprc, buyprc])/2)
    if len(avgprc) < 12:
        return
    if len(avgprc) == 12:
        reading12ema = np.insert(reading12ema, 0, sum(avgprc)/12)
        return
    if len(avgprc) < 20:
        newval = (avgprc[0] -  reading12ema[0]) * 2/13 + reading12ema[0]
        reading12ema = np.insert(reading12ema, 0, newval)
        return
    if len(avgprc) == 20:
        reading20ema = np.insert(reading20ema, 0, sum(avgprc)/20)
        newval = (avgprc[0] -  reading12ema[0]) * 2/13 + reading12ema[0]
        reading12ema = np.insert(reading12ema, 0, newval)
        micromacd = reading12ema[0] - reading20ema[0]
        if micromacd > 0.15:
            return np.array([['buy', sellprc, int(curhold/3)]])
        if micromacd < -0.15:
            return np.array([['sell', buyprc, int(curhold/3)]])
    if len(avgprc) > 20:
        newval20 = (avgprc[0] - reading20ema[0]) * 2/21 + reading20ema[0]
        reading20ema = np.insert(reading20ema, 0, newval20)
        newval12 = (avgprc[0] - reading12ema[0]) * 2/13 + reading12ema[0]
        reading12ema = np.insert(reading12ema, 0, newval12)
        micromacd = reading12ema[0] - reading20ema[0]
        if micromacd > 0.15:
            return np.array([['buy', sellprc, int(curhold/3)]])
        if micromacd < -0.15:
            return np.array([['sell', buyprc, int(curhold/3)]])
