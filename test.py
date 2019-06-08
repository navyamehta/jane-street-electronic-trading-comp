#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x client.py
# 3) Run in loop: while true; do ./client.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time
import numpy as np
from math import ceil

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="panipuristreet"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# ~~~~~============== MAIN LOOP ==============~~~~~
# rm client.py && nano client.py

def micromacd (sellprc, buyprc, curhold, avgprc, reading12ema, reading20ema):
    avgprc = np.insert(avgprc, 0, sum([sellprc, buyprc])/2)
    # print(len(avgprc))
    if len(avgprc) < 12:
        return [], avgprc, reading12ema, reading20ema
    if len(avgprc) == 12:
        reading12ema = np.insert(reading12ema, 0, sum(avgprc)/12)
        return [], avgprc, reading12ema, reading20ema
    if len(avgprc) < 20:
        newval = (avgprc[0] - reading12ema[0]) * 2/13 + reading12ema[0]
        reading12ema = np.insert(reading12ema, 0, newval)
        return [], avgprc, reading12ema, reading20ema
    if len(avgprc) == 20:
        reading20ema = np.insert(reading20ema, 0, sum(avgprc)/20)
        newval = (avgprc[0] - reading12ema[0]) * 2/13 + reading12ema[0]
        reading12ema = np.insert(reading12ema, 0, newval)
        micromacd = reading12ema[0] - reading20ema[0]
        # print(reading12ema[0])
        # print(reading20ema[0])
        # print(micromacd)
        # print("---------")
        # time.sleep(2)
        if micromacd > 0.1:
            return np.array([['buy', sellprc, abs(ceil(curhold/3))]]), avgprc, reading12ema, reading20ema
        if micromacd < -0.1:
            if curhold!=0:
                return np.array([['sell', buyprc, abs(ceil(curhold/3))]]), avgprc, reading12ema, reading20ema
            else:
                return np.array([['sell', buyprc, 5]]), avgprc, reading12ema, reading20ema
        else:
            return [], avgprc, reading12ema, reading20ema
    if len(avgprc) > 20:
        newval20 = (avgprc[0] - reading20ema[0]) * 2/21 + reading20ema[0]
        reading20ema = np.insert(reading20ema, 0, newval20)
        newval12 = (avgprc[0] - reading12ema[0]) * 2/12 + reading12ema[0]
        reading12ema = np.insert(reading12ema, 0, newval12)
        # print(reading12ema[0])
        # print(reading20ema[0])
        micromacd = reading12ema[0] - reading20ema[0]
        # print(micromacd)
        # print("-----------------")
        # time.sleep(2)
        if micromacd > 0.1:
            return np.array([['buy', sellprc, abs(ceil(curhold/3))]]), avgprc, reading12ema, reading20ema
        if micromacd < -0.1:
            if curhold!=0:
                return np.array([['sell', buyprc, abs(ceil(curhold/3))]]), avgprc, reading12ema, reading20ema
            else:
                return np.array([['sell', buyprc, 5]]), avgprc, reading12ema, reading20ema
        else:
            return [], avgprc, reading12ema, reading20ema

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})

    # buy_order = {"type": "add", "order_id": 5, "symbol": "BOND", "dir": "BUY", "price": 1000, "size": 20}
    # write_to_exchange(exchange, buy_order)
    # [[1001, 7], [1002, 2]]

    current_bonds = 0

    order_id = 0
    TIMEOUT = 2

    total_orders_cancel = 0

    tot_orders_buy = {}

    total_orders_buy = 0
    exec_orders_buy = 0
    success_orders_buy = 0

    total_orders_sell = 0
    exec_orders_sell = 0
    success_orders_sell = 0

    to_send = {}
    working_id = 0
    trying = False
    hello = False

    holdings = {}
    lag_orders = 1

    avgprc_all = {}
    reading12ema_all = {}
    reading20ema_all = {}

    counter = 0
    while True:
        try:
            res_from_exchange = read_from_exchange(exchange)
        except:
            continue
        # print("The exchange replied:", res_from_exchange, file=sys.stderr)
        # print("\n")

        res_type = res_from_exchange["type"]
        if res_type == "hello":
            # print(res_from_exchange)
            symbols = res_from_exchange["symbols"]
            for symbol in symbols:
                avgprc_all[symbol["symbol"]] = np.array([])
                reading12ema_all[symbol["symbol"]] = np.zeros(11)
                reading20ema_all[symbol["symbol"]] = np.zeros(19)
                holdings[symbol["symbol"]] = symbol["position"]
            print(holdings)
            time.sleep(TIMEOUT)
        elif res_type == "open":
            pass
        elif res_type == "book":
            counter += 1

            if counter == lag_orders:
                counter = 0
                symbol = res_from_exchange["symbol"]

                buy_res = res_from_exchange["buy"]
                sell_res = res_from_exchange["sell"]

                buy_prices = []
                buy_amounts = []

                sell_prices = []
                sell_amounts = []


                for order in buy_res:
                    buy_prices.append(order[0])
                    buy_amounts.append(order[1])

                for order in sell_res:
                    sell_prices.append(order[0])
                    sell_amounts.append(order[1])


                if len(buy_prices) > 0:
                    max_buy_price = max(buy_prices)
                if len(sell_prices) > 0:
                    min_sell_price = min(sell_prices)
                else:
                    min_sell_price = max_buy_price
                if len(buy_prices) == 0:
                    max_buy_price = min_sell_price



                highest_id = -1
                highest_buy = 0
                for key, value in to_send.iteritems():
                    if value["dir"] == "BUY":
                        if value["price"] > highest_buy:
                            highest_id = value["order_id"]
                            highest_buy = value["price"]

                if symbol == "BOND":
                    pass
                else:
                    # print("MICRO")
                    order_data, new_avgrprice, new_12, new_20 = micromacd(min_sell_price, max_buy_price, holdings[symbol], avgprc_all[symbol], reading12ema_all[symbol], reading20ema_all[symbol])
                    # print(order_data)
                    # print(new_avgrprice)
                    # print(new_12)
                    # print(new_20)
                    avgprc_all[symbol] = new_avgrprice
                    reading12ema_all[symbol] = new_12
                    reading20ema_all[symbol] = new_20
                    if len(order_data) > 0:
                        orders = order_data.tolist()
                        for order in orders:
                            if order[0] == "buy":
                                build = {"type": "add", "order_id": order_id, "symbol": symbol, "dir": "BUY", "price": int(float(order[1])), "size": int(float(order[2]))}
                                total_orders_buy += 1
                            elif order[0] == "sell":
                                build = {"type": "add", "order_id": order_id, "symbol": symbol, "dir": "SELL", "price": int(float(order[1])), "size": int(float(order[2]))}
                                total_orders_sell += 1
                            elif order[0] == "cancel":
                                build = {"type": "cancel", "order_id": int(order[2])}
                                total_orders_cancel += 1
                            # print(build)
                            to_send[order_id] = build
                            order_id += 1
                            # to_send.append(build)
        elif res_type == "fill":
            if res_from_exchange["dir"] == "BUY":
                success_orders_buy += 1
            elif res_from_exchange["dir"] == "SELL":
                success_orders_sell += 1
            print(res_from_exchange)
            del to_send[res_from_exchange["order_id"]]
            # write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
            # hello = True
            time.sleep(TIMEOUT)
        elif res_type == "reject":
            print(res_from_exchange)
            time.sleep(TIMEOUT)
        elif res_type == "error":
            print(res_from_exchange)
            time.sleep(TIMEOUT)
        elif res_type == "ack":
            print(res_from_exchange)
            if to_send[res_from_exchange["order_id"]]["dir"] == "BUY":
                exec_orders_buy += 1
            elif to_send[res_from_exchange["order_id"]]["dir"] == "SELL":
                exec_orders_sell += 1
            working_id += 1
            trying = False
            time.sleep(TIMEOUT)

        print("--------------------")

        print("TOTAL ORDERS BUY:")
        print(total_orders_buy)
        print("EXEC ORDERS BUY:")
        print(exec_orders_buy)
        print("SUCCESS ORDERS BUY:")
        print(success_orders_buy)

        print("--------------------")
        print("TOTAL ORDERS SELL:")
        print(total_orders_sell)
        print("EXEC ORDERS SELL:")
        print(exec_orders_sell)
        print("SUCCESS ORDERS SELL:")
        print(success_orders_sell)

        print("--------------------")

        print("TOTAL ORDERS CANCEL:")
        print(total_orders_cancel)

        if working_id == 0:
            if to_send and not trying and not hello:
                print(to_send[working_id])
                write_to_exchange(exchange, to_send[working_id])
                trying = True
        else:
            if not trying and not hello:
                write_to_exchange(exchange, to_send[working_id])
                trying = True
        hello = False

        print("\n\n")


if __name__ == "__main__":
    main()
