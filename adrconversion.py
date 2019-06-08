# Takes price values from VALBZ, and trades in direction of spread between two
# Convert price is constant regardless of number of shares
# Want to trade largest orders as possible to minimize conversion cost
# 4 ways, going from ADR to normal and within you can short or buy



# 1 - Buying VALE ADR

def buy_adr(sellprc_adr, sellamt_adr, buyprc_adr, buyamt_adr, sellprc, sellamt, buyprc, buyamt, curhold_adr, curhold):
    conversion_cost = 10
    shortlim = -6
    longlim = 6
    for i in range (0, len(sellamt_adr)):
        if (sellprc_adr[i] > buyprc[i]):
            spread = sellprc_adr[i] - buyprc[i]
            if (spread * sellamt_adr[i] > 10):
                amt_we_buy = max(ceiling(10/spread), min(sellamt_adr[i], abs(longlim-curhold)))
                orders.append(['buy', sellprc_adr[i], amt_we_buy])

# 2 - Selling VALE ADR

def sell_adr(sellprc_adr, sellamt_adr, buyprc_adr, buyamt_adr, sellprc, sellamt, buyprc, buyamt, curhold_adr, curhold):
    conversion_cost = 10
    shortlim = -6
    longlim = 6
    for i in range (0, len(buyamt_adr)):               
        if (buyprc_adr[i] > sellprc[i]):
            spread = buyprc_adr[i] - sellprc[i]
                if (spread * buyamt_adr[i] > 10):
                    amt_we_sell = max(ceiling(10/spread), min(buyamt_adr[i], abs(longlim-curhold)))
                    orders.append(['sell', buyprc_adr[i], amt_we_sell])

# 3 - Buying VALBZ

def buy_adr(sellprc_adr, sellamt_adr, buyprc_adr, buyamt_adr, sellprc, sellamt, buyprc, buyamt, curhold_adr, curhold):
    for i in range (0, len(sellamt)):               
        if (buyprc_adr[i] < sellprc[i]):
            spread = sellprc[i] - buyprc_adr[i] 
            if (spread * sellamt[i] > 10)
                amt_we_buy = max(ceiling(10/spread), min(sellamt[i], abs(longlim-curhold)))
                orders.append(['buy', sellprc[i], amt_we_buy])


# 4 - Selling VALBZ
def selling_adr(sellprc_adr, sellamt_adr, buyprc_adr, buyamt_adr, sellprc, sellamt, buyprc, buyamt, curhold_adr, curhold):
    for i in range (0, len(buyamt)):
        if (sellprc_adr[i] < buyprc[i]):
            spread = buyprc[i] - sellprc_adr[i])
            if (spread * buyamt[i] > 10)
                amt_we_sell = max(ceiling(10/spread), min(buyamt[i], abs(longlim-curhold)))
                orders.append(['sell', buyprc[i], amt_we_sell])

# 5 - Converting VALE to VALBZ and vice versa
def conversion(curhold_adr, curhold)
    for i in range (0, curhold_adr):
            orders.append(['convert', "VALE", "SELL", curhold_ADR)

    for i in range (0, curhold):
            orders.append(['convert', "VALBZ", "BUY", curhold)
                

    
