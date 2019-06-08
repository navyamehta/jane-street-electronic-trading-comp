import numpy as np
import pandas as pd

def bondtrade(sellprc, sellamt, buyprc, buyamt, curhold):
    accepprc = 1000
    sellamt = sellamt[sellprc < accepprc]
    sellprc = sellprc[sellprc < accepprc]
    buyamt = buyamt[buyprc > accepprc]
    buyprc = buyprc[buyprc > accepprc]
    newbuyval = 0
    newsellval = 0
    for i in range(0, len(sellamt)):
        newbuyval += sellprc[i] * sellamt[i]
    for i in range(0, len(buyamt)):
        newsellval += buyprc[i] * buyamt[i]
    shortlim = -65
    longlim = 65
    orders = np.array([])
    for i in range(0, len(sellamt)):
        amt = min(sellamt[i], abs(longlim-curhold))
        amt = max(0, amt)
        orders = np.append(orders, np.array([['buy', sellprc[i], amt]])).reshape(-3,3)
    #Irrational orders clear automatically i.e. you cant have buy above acceplim and sell below acceplim
    for i in range(0, len(buyamt)):
        amt = min(buyamt[i], abs(shortlim-curhold))
        amt = max(0, amt)
        orders = np.append(orders, np.array([['sell', buyprc[i], amt]])).reshape(-3,3)
    return [orders, newbuyval, newsellval]
