#For simulation, we have an ETF that can be dismantled into its individual components. Here, we can leverage arbitrage, and
#analyze whether we must build or break ETF packages. 

#The cvrt function converts sell prices and amounts into an num-value average, with num being its amount in the ETF package.
#Subsequently, we compare the ETF fair price to its current trading price and use a boolean to decide whether it is profitable
#to change the state.

import pandas as pd
import numpy as np

def cvrt(sellprc, sellamt, num):
    sellprc = sellprc.repeat(sellamt)
    sellprc = pd.Series(sellprc).sort_values().cumsum().reset_index(drop=True)
    val = pd.Series(np.arange(sum(sellamt)))
    sellprc = sellprc - sellprc.where((val+1) % num == 0).shift(1).ffill().fillna(0)
    sellprc = sellprc.where((val+1) % num == 0).dropna().values
    sellprc = sellprc/num
    return sellprc.astype('float64').astype('int')


def etfcvrt(bondsellprc, bondsellamt, gssellprc, gssellamt, mssellprc, mssellamt, wfcsellprc, wfcsellamt, etfbuyprc, etfbuyamt):
    bondcvrt = cvrt(bondsellprc, bondsellamt, 3)
    gscvrt = cvrt(gssellprc, gssellamt, 2)
    mscvrt = cvrt(mssellprc, mssellamt, 3)
    wfccvrt = cvrt(wfcsellprc, wfcsellamt, 2)
    buycvrt = cvrt(etfbuyprc, etfbuyamt, 10)
    finallen = min(len(bondcvrt), len(gscvrt), len(mscvrt), len(wfccvrt), len(buycvrt))
    if finallen == 0:
        return
    bondcvrt = bondcvrt[:finallen]
    gscvrt = gscvrt[:finallen]
    mscvrt = mscvrt[:finallen]
    wfccvrt = wfccvrt[:finallen]
    buycvrt = buycvrt[:finallen]
    etffairprc = np.zeros(finallen)
    for i in range(0, finallen):
        etffairprc[i] = 3 * bondcvrt[i] + 2 * gscvrt[i] + 3 * mscvrt[i] + 2 * wfccvrt[i]
    etffairprc = etffairprc/10
    etffairprc = etffairprc[etffairprc < buycvrt].astype('float64')
    print(sum(buycvrt))
    print(sum(etffairprc))
    if (len(etffairprc) > 0) & (sum(etffairprc) + 11 < sum(buycvrt)):
        orders = np.array([['buy', min(bondsellprc), len(etffairprc) * 3, 'BOND'], ['buy', min(gssellprc), len(etffairprc) * 2, 'GS'], 
                          ['buy', min(mssellprc), len(etffairprc) * 3, 'MS'], ['buy', min(wfccvrt), len(etffairprc) * 2, 'WFC'],
                          ['convert', 'XLF', 'buy', len(etffairprc) * 10], ['sell', max(etfbuyprc), len(etffairprc) * 10, 'XLF'])
        return orders
    else:
        return []
    
