
def bondtrade(sellprc, sellamt, buyprc, buyamt, curhold):
	shortlim = -100
	longlim = 100
	accepprc = 1000
	sellamt = sellamt[sellprc < accepprc]
	sellprc = sellprc[sellprc < accepprc]
	buyamt = buyamt[buyprc > accepprc]
	buyprc = buyprc[buyprc > accepprc]
	orders = []
	for i in range(0, len(sellamt)):
		amt = min(sellamt[i], abs(longlim-curhold))
		orders.append(['buy', sellprc[i], amt])
	#Irrational orders clear automatically i.e. you cant have buy above acceplim and sell below acceplim
	for i in range(0, len(buyamt)):
		amt = min(buyamt[i], abs(shortlim-curhold))
		orders.append(['sell', buyprc[i], amt])
	return orders