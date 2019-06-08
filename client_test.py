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
from adrconversion import buy_adr

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

    order_id = 0
    TIMEOUT = 5

    total_orders_cancel = 0

    total_orders_buy = 0
    success_orders_buy = 0

    total_orders_sell = 0
    success_orders_sell = 0

    to_send = {}
    working_id = 0
    trying = False
    hello = False

    holdings = {}
    lag_orders = 200

    counter = 0
    store_value = []
    while True:
        try:
            res_from_exchange = read_from_exchange(exchange)
        except:
            continue
        print("The exchange replied:", res_from_exchange, file=sys.stderr)
        # print("\n")

        res_type = res_from_exchange["type"]
        if res_type == "hello":
            # print(res_from_exchange)
            symbols = res_from_exchange["symbols"]
            for symbol in symbols:
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

                if symbol == "BOND":
                    pass
                else:
                    print(symbol)
                    if symbol == "VALE":
                        store_value = [sell_prices, sell_amounts, holdings[symbol]]
                    elif symbol == "VALBZ":
                        if store_value:
                            orders = buy_adr(store_value[0], store_value[1], buy_prices, buy_amounts, store_value[2])
                            import pdb; pdb.set_trace()
                            print(orders)
                            if orders:
                                for order in orders:
                                    if order[0] == "buy":
                                        build = {"type": "add", "order_id": order_id, "symbol": symbol, "dir": "BUY", "price": int(order[1]), "size": int(order[2])}
                                        total_orders_buy += 1
                                    elif order[0] == "sell":
                                        build = {"type": "add", "order_id": order_id, "symbol": symbol, "dir": "SELL", "price": int(order[1]), "size": int(order[2])}
                                        total_orders_sell += 1
                                to_send[order_id] = build
                                order_id += 1
                            time.sleep(TIMEOUT)

        elif res_type == "fill":
            if res_from_exchange["dir"] == "BUY":
                if res_from_exchange["symbol"] == "VALE":
                    build_convert = {"type": "convert", "order_id": res_from_exchange["order_id"], "symbol": "VALE", "dir": "SELL", "size": holdings["VALE"]}
                    order_id += 1
                    to_send[order_id] = build_convert
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
            working_id += 1
            trying = False
            time.sleep(TIMEOUT)

        # print("--------------------")

        # print("TOTAL ORDERS BUY:")
        # print(total_orders_buy)
        # print("SUCCESS ORDERS BUY:")
        # print(success_orders_buy)

        # print("--------------------")
        # print("TOTAL ORDERS SELL:")
        # print(total_orders_sell)
        # print("SUCCESS ORDERS SELL:")
        # print(success_orders_sell)

        # print("--------------------")

        # print("TOTAL ORDERS CANCEL:")
        # print(total_orders_cancel)

        if working_id == 0:
            if to_send and not trying and not hello:
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
