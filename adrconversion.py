# Takes price values from VALBZ, and trades in direction of spread between two
# Convert price is constant regardless of number of shares
# Want to trade largest orders as possible to minimize conversion cost
# 4 ways, going from ADR to normal and within you can short or buy



# 1 - Buying VALE ADR, converting to VALBZ,  selling VALBZ,

import math

# Need to make spread per stock
def buy_adr(sellprc_adr, sellamt_adr, buyprc, buyamt, curhold_adr):
    conversion_cost = 10
    shortlim = -6
    longlim = 6
    orders = []
    ask_per_unit = []
    bid_per_unit = []

    # lowest_ask = 0
    # highest_bid = 0
    if len(sellprc_adr) > 0 and len(buyprc) > 0:
        lowest_ask = min(sellprc_adr)
        highest_bid = max(buyprc)
        spread = abs(highest_bid - lowest_ask)
        # print(spread)

        for i in range (0, len(sellamt_adr)):
            if (highest_bid < lowest_ask):
                if (spread * sellamt_adr[i] > 10):
                    amt_we_buy = max(math.ceil(10/spread), min(sellamt_adr[i], abs(longlim-curhold_adr)))
                    orders.append(['buy', lowest_ask, amt_we_buy, "VALE"])
                    orders.append(['convert', "VALE", "SELL", amt_we_buy])
                    orders.append(['sell', highest_bid, amt_we_buy, "VALBZ"])

        for i in range (0, len(buyamt)):
            if (highest_bid > lowest_ask):
                if (spread * buyamt[i] > 10):
                    amt_we_sell = max(math.ceil(10/spread), min(buyamt[i], abs(longlim-curhold_adr)))
                    orders.append(['sell', highest_bid, amt_we_sell, "VALBZ"])
                    orders.append(['convert', "VALE", "BUY", amt_we_sell])
                    orders.append(['buy', lowest_ask, amt_we_sell, "VALE"])

        return orders
    return []

# 2 - Buying VALBZ, converting to VALE, selling VALE

def sell_adr(buyprc_adr, buyamt_adr, sellprc, sellamt, curhold):
    conversion_cost = 10
    shortlim = -6
    longlim = 6
    for i in range (0, len(buyamt_adr)):
        if (sellprc[i] < buyprc[i]):
            spread = abs(buyprc_adr[i] - sellprc[i])
            if (spread * buyamt_adr[i] > 10):
                    amt_we_buy = max(ceiling(10/spread), min(sellamt[i], abs(longlim-curhold)))
                    orders.append(['buy', sellprc[i], amt_we_buy])
                    if (fill):
                        orders.append(['convert', "VALE", "BUY", curhold])
                    amt_we_sell = max(ceiling(10/spread), min(buyamt_adr[i], abs(longlim-curhold)))
                    orders.append(['sell', buyprc_adr[i], amt_we_sell])