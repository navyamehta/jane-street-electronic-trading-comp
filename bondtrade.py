#In addition to the old bond strategy earlier, we also add functionality to place cursory orders that are ideally profitable.
#However, if a better price is detected, we nullify said orders and improve market standing
import numpy as np
import pandas as pd

def bondtrade(sellprc, sellamt, buyprc, buyamt, curhold, incbuy, incsell, fill=0):
    accepprc = 1000
    shortlim = -80
    longlim = 80
    orders = np.array([])
    if len(sellprc) == 0:
        statsell = 1002
    else:
        statsell = max(1002, min(sellprc) - 1)
    if len(buyprc) == 0:
        statbuy = 998
    else:
        statbuy = min(998, max(buyprc) + 1)
    sellamt = sellamt[sellprc < accepprc]
    sellprc = sellprc[sellprc < accepprc]
    buyamt = buyamt[buyprc > accepprc]
    buyprc = buyprc[buyprc > accepprc]
    newbuyval = 0
    newsellval = 0
    for i in range(0, len(sellamt)):
        newbuyval += sellprc[i] * sellamt[i]
    newbuyval += statbuy * 10
    for i in range(0, len(buyamt)):
        newsellval += buyprc[i] * buyamt[i]
    newsellval += statsell * 10
    #We only need to nullify an inefficient old buy order, since if a sell order is below the lowest buy, it is still executed
    #by the marketplace at aforementioned buy price
    if isinstance(fill, list) & (len(sellprc) > 0):
        cnc = cancel(sellprc, sellamt, curhold, fill)
        orders = np.append(orders, cnc).reshape(-3,3)
    for i in range(0, len(sellamt)):
        amt = min(sellamt[i], abs(longlim-curhold))
        amt = max(0, amt)
        orders = np.append(orders, np.array([['buy', sellprc[i], amt]])).reshape(-3,3)
    for i in range(0, len(buyamt)):
        amt = min(buyamt[i], abs(shortlim-curhold))
        amt = max(0, amt)
        orders = np.append(orders, np.array([['sell', buyprc[i], amt]])).reshape(-3,3)
    if (curhold+incbuy)<(longlim-1):
        orders = np.append(orders, np.array([['buy', statbuy, 1]])).reshape(-3,3)
    if (curhold-incsell) > (shortlim+1):
        orders = np.append(orders, np.array([['sell', statsell, 1]])).reshape(-3,3)
    return [orders, newbuyval, newsellval]


def cancel(prc, amt, hold, fill):
    if fill[0] < min(prc):
        return np.array([])
    else:
        return np.array(['cancel', fill[0], fill[1]])