#We implement pennying, in an attempt to close the buy-sell spread and try to have our trades picked up by the marketplace
#by price-insensitive investors

import pandas as pd
import numpy as np

def pennying(iden, sellprc, buyprc, curhold, incbuy, incsell):
    longlim = pd.Series(iden).apply(lambda s: 10 if s in ['VALBZ', 'VALE'] else 100).values[0]/1.5
    shortlim = - longlim
    orders = np.array([])
    if (curhold + incbuy) < (longlim-1):
        if (len(buyprc)!=0):
            prc = max(buyprc)
            orders = np.append(orders, [['buy', prc+1, 1]]).reshape(-3,3)
    if (curhold + incsell) > (shortlim+1):
        if (len(sellprc)) != 0:
            prc = min(sellprc)
            orders = np.append(orders, [['sell', prc-1, 1]]).reshape(-3,3)
    return orders
