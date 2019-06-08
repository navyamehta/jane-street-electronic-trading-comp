#This strategy assumes that the market behaves rationally and thus you cannot have sell orders below an arbitrary
#acceptable limit and also have buy orders above. Thus, this code currently does not run against itself, and instead
#only reads the best clearing price in the market. It executes orders to perfectly match amounts on the list as
#it does not currently have cancel functionality
def bondtrade(sellprc, sellamt, buyprc, buyamt, curhold, fill=0):
    accepprc = 1000
    shortlim = -65
    longlim = 65
    orders = np.array([])
    statsell = max(1002, min(sellprc) - 1)
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
    if isinstance(fill, list):
        if fill[0] == 'buy':
            cnc = cancel(sellprc, sellamt, curhold, fill)
        else:
            cnc = cancel(buyprc, buyamt, curhold, fill)
        orders = np.append(orders, cnc).reshape(-3,3)
    for i in range(0, len(sellamt)):
        amt = min(sellamt[i], abs(longlim-curhold))
        amt = max(0, amt)
        orders = np.append(orders, np.array([['buy', sellprc[i], amt]])).reshape(-3,3)
    for i in range(0, len(buyamt)):
        amt = min(buyamt[i], abs(shortlim-curhold))
        amt = max(0, amt)
        orders = np.append(orders, np.array([['sell', buyprc[i], amt]])).reshape(-3,3)
    orders = np.append(orders, np.array([['sell', statsell, 10]])).reshape(-3,3)
    orders = np.append(orders, np.array([['buy', statbuy, 10]])).reshape(-3,3)
    return [orders, newbuyval, newsellval]
