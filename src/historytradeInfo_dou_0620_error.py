# coding=utf-8
#
# date：日期
# open：开盘价
# high：最高价
# close：收盘价
# low：最低价
# volume：成交量
# price_change：价格变动
# p_change：涨跌幅
# ma5：5
# 日均价
# ma10：10
# 日均价
# ma20:20
# 日均价
# v_ma5:5
# 日均量
# v_ma10:10
# 日均量
# v_ma20:20
# 日均量
# turnover:换手率[注：指数无此项]


import tushare as ts
from pymongo import MongoClient
import json
import pandas as pd
import numpy as np
import datetime
import time
# 82214039a3bfd40645b630b18a46151509f4a4bbde00dbbd60ee3585
# 30abde40af1725d6670ea349b624e31bbf8a50022c25de8ec9da4f53
ts.set_token('82214039a3bfd40645b630b18a46151509f4a4bbde00dbbd60ee3585')

def getcodeList():
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.test8
    stockCodeList = []
    for item in db.stockCode.find():
        code = item.get('SYMBOL')
        if code not in stockCodeList:
            stockCodeList.append(code)
    return stockCodeList

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.test8
codeList = getcodeList()



def insert_hisData():
    for code in codeList:
        # time.sleep(0.15)
        if code == '' or code is None:
            continue
        else:
            code_str = code
            if code == '001270':
                print(code)
            if code_str[0:2] == "00" or code_str[0:2] == "30":
                code_str = code_str + ".SZ"
            else:
                code_str = code_str + ".SH"
            search_set = db.historytradeInfoPro
            start_date = datetime.datetime.now().strftime('%Y%m%d')
            if search_set.find_one({"ts_code": code_str, "trade_date" : start_date}) == None:
                pro = ts.pro_api()
                df = pro.daily(ts_code=code_str, start_date=datetime.datetime.now().strftime('%Y%m%d'),end_date=datetime.datetime.now().strftime('%Y%m%d'))
                # df = pro.daily(ts_code=code_str, start_date='20220910', end_date='20220914')
                try:
                    df1 =df.reset_index()
                except Exception:
                    print('NoneType object has no attribute reset_index')
                # print df
                if df1 is None:
                    continue
                else:
                    df1['code'] = code
                    try:
                        db.historytradeInfoPro.insert_many(json.loads(df1.to_json(orient='records')))
                    except Exception:
                        print(df1['code'])



insert_hisData()

