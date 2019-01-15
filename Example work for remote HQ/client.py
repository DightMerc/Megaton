#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some functions: fetch_trades_history, fetch_candles in OKEx platform
Author: dightmerc@gmail.com
"""


from requests import post, get
from collections import namedtuple
import json



def fetch_trades_history(api_key, symbol, status, current_page, page_length, sign):
    """
    api_key	apiKey of the user
    symbol	Pairs like : ltc_btc etc_btc
    status	query type: 0 for unfilled (open) orders, 1 for filled orders
    current_page	current page number
    page_length	number of orders returned per page, maximum 200
    sign	signature of request parameters
    """
    try:

        payload = {
            'api_key': str(api_key),
            'symbol': str(symbol),
            'status': int(status),
            'current_page': int(current_page),
            'page_length': int(page_length),
            'sign': sign
            }

        request = post("https://www.okex.com/api/v1/order_history.do", data=payload)

        if request.text!="":
            data = json.loads(request, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            
            return data
        else:
            return "empty"
    except Exception as e:

        error = format("Error: %s",str(e)) 
        print(error)

        return error

def fetch_candles(symbol, type, size, since):
    """
    symbol	Pairs like : ltc_btc etc_btc
    type	1min/3min/5min/15min/30min/1day/1week/1hour/2hour/4hour/6hour/12hour
    size	specify data size to be acquired
    since	timestamp(eg:1417536000000). data after the timestamp will be returned
    """
    try:

        payload = {
            'symbol': str(symbol),
            'type': str(type),
            'size': int(size),
            'since': int(since)
            }

        request = get('https://www.okex.com/api/v1/kline.do', params=payload)

        if request.text!="":
            data = json.loads(request, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            
            return data
        else:
            return "empty"
    except Exception as e:

        error = format("Error: %s",str(e)) 
        print(error)

        return error