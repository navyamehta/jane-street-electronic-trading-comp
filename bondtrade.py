#This strategy assumes that the market behaves rationally and thus you cannot have sell orders below an arbitrary
#acceptable limit and also have buy orders above that. In that regard, both for loops will not run in the code
#under traditional market circumstances
def bondtrade(sellprc, sellamt, buyprc, buyamt, curhold):
	shortlim = -100
	longlim = 100
	accepprc = 1000
	sellamt = sellamt[sellprc < accepprc]
	sellprc = sellprc[sellprc < accepprc]
	buyamt = buyamt[buyprc > accepprc]
	buyprc = buyprc[buyprc > accepprc]
	orders = []
	#We check how . many current sell orders are below fair value, and how many buys are above
	for i in range(0, len(sellamt)):
		amt = min(sellamt[i], abs(longlim-curhold))
		orders.append(['buy', sellprc[i], amt])
	for i in range(0, len(buyamt)):
		amt = min(buyamt[i], abs(shortlim-curhold))
		orders.append(['sell', buyprc[i], amt])
	return orders
