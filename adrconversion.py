# Takes price values from VALBZ, and trades in direction of spread between two
# Convert price is constant regardless of number of shares
# Want to trade largest orders as possible to minimize conversion cost
# 4 ways, going from ADR to normal and within you can short or buy



# 1 - Buying VALE ADR, converting to VALBZ,  selling VALBZ,

from math import ceil

def buy_adr(sellprc_adr, sellamt_adr, buyprc, buyamt, curhold_adr):
    conversion_cost = 10
    shortlim = -6
    longlim = 6
    orders = []
    for i in range (0, min(len(sellprc_adr), len(buyprc))):
        if (sellprc_adr[i] < buyprc[i]):
            spread = abs(sellprc_adr[i] - buyprc[i])
            if (spread * sellamt_adr[i] > 10):
                amt_we_buy = max(ceil(10/spread), min(sellamt_adr[i], abs(longlim-curhold_adr)))
                orders.append(['buy', sellprc_adr[i], amt_we_buy])
                # if (fill):
                #     orders.append(['convert', "VALE", "SELL", curhold_adr_adr)
                amt_we_sell = max(ceil(10/spread), min(buyamt[i], abs(longlim-curhold_adr)))
                orders.append(['sell', buyprc[i], amt_we_sell])

    return orders

# 2 - Buying VALBZ, converting to VALE, selling VALE

# def sell_adr(sellprc_adr, sellamt_adr, buyprc_adr, buyamt_adr, sellprc, sellamt, buyprc, buyamt, curhold_adr_adr, curhold_adr, fill):
#     conversion_cost = 10
#     shortlim = -6
#     longlim = 6
#     for i in range (0, len(buyamt_adr)):
#         if (sellprc[i] < buyprc[i]):
#             spread = abs(buyprc_adr[i] - sellprc[i])
#                 if (spread * buyamt_adr[i] > 10):
#                     amt_we_buy = max(ceiling(10/spread), min(sellamt[i], abs(longlim-curhold_adr)))
#                     orders.append(['buy', sellprc[i], amt_we_buy])
#                     if (fill):
#                         orders.append(['convert', "VALBZ", "BUY", curhold_adr)
#                     amt_we_sell = max(ceiling(10/spread), min(buyamt_adr[i], abs(longlim-curhold_adr)))
#                     orders.append(['sell', buyprc_adr[i], amt_we_sell])




