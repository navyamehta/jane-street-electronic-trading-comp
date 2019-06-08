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
from bondtrade import bondtrade
from pennying import pennying

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

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})

    # buy_order = {"type": "add", "order_id": 5, "symbol": "BOND", "dir": "BUY", "price": 1000, "size": 20}
    # write_to_exchange(exchange, buy_order)
    # [[1001, 7], [1002, 2]]

    current_bonds = 0

    order_id = 1
    TIMEOUT = 5

    total_orders_buy = 0
    success_orders_buy = 0

    total_orders_sell = 0
    success_orders_sell = 0

    to_send = []
    working_id = 0
    trying = False
    while True:
        try:
            res_from_exchange = read_from_exchange(exchange)
        except:
            continue
        # print("The exchange replied:", res_from_exchange, file=sys.stderr)
        # print("\n")

        res_type = res_from_exchange["type"]
        if res_type == "hello":
            symbols = res_from_exchange["symbols"]
            for symbol in symbols:
                if symbol["symbol"] == "BOND":
                    current_bonds = symbol["position"]
                    print(current_bonds)
                    time.sleep(TIMEOUT)
        elif res_type == "open":
            pass
        elif res_type == "book":
            symbol = res_from_exchange["symbol"]

            if symbol == "BOND":

                buy_res= res_from_exchange["buy"]
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

                order_data = bondtrade(np.array(sell_prices), np.array(sell_amounts), np.array(buy_prices), np.array(buy_amounts), current_bonds, total_orders_buy-success_orders_buy, total_orders_sell-success_orders_sell)
                orders = order_data[0].tolist()

                build = {}
                # print("# Orders (OURS): ")
                # print(len(orders))
                for order in orders:
                    if order[0] == "buy":
                        build = {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", "price": int(order[1]), "size": int(order[2])}
                        total_orders_buy += 1
                    elif order[0] == "sell":
                        build = {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": int(order[1]), "size": int(order[2])}
                        total_orders_sell += 1
                    order_id += 1
                    print(build)
                    to_send.append(build)
            else:
                orders = pennying(symbol, np.array(sell_prices), np.array(buy_prices), total_orders_buy-success_orders_buy, total_orders_sell-success_orders_sell)
                for order in orders:
                    if order[0] == "buy":
                        build = {"type": "add", "order_id": order_id, "symbol": symbol, "dir": "BUY", "price": int(order[1]), "size": int(order[2])}
                        total_orders_buy += 1
                    elif order[0] == "sell":
                        build = {"type": "add", "order_id": order_id, "symbol": symbol, "dir": "SELL", "price": int(order[1]), "size": int(order[2])}
                        total_orders_sell += 1
                    order_id += 1
                    print(build)
                    to_send.append(build)
        elif res_type == "fill":
            if res_from_exchange["dir"] == "buy":
                success_orders_buy += 1
            elif res_from_exchange["dir"] == "sell":
                success_orders_sell += 1
            print(res_from_exchange)
            time.sleep(TIMEOUT)
        elif res_type == "reject":
            print(res_from_exchange)
            time.sleep(TIMEOUT)
        elif res_type == "error":
            print(res_from_exchange)
            time.sleep(TIMEOUT)
        elif res_type == "ack":
            print(res_from_exchange)
            working_id += 1
            trying = False
            time.sleep(TIMEOUT)

        if working_id == 0:
            if len(to_send) > 0 and not trying:
                write_to_exchange(exchange, to_send[working_id])
                trying = True
        else:
            if not trying:
                write_to_exchange(exchange, to_send[working_id])
                trying = True


if __name__ == "__main__":
    main()
