# coding=utf-8

import tushare as ts
from pymongo import MongoClient
import json
import datetime
import time
import numpy

ts.set_token('82214039a3bfd40645b630b18a46151509f4a4bbde00dbbd60ee3585')

# pro = ts.pro_api()
#
# df = pro.index_daily(ts_code='399300.SZ')
#
# #或者按日期取
#
# df = pro.index_daily(ts_code='399300.SZ', start_date='20180101', end_date='20181010')


def getcodeList():
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.test8
    stockCodeList = []
    for item in db.stockCode.find():
        code = item.get('SYMBOL')
        if code not in stockCodeList:
            stockCodeList.append(code)
    return stockCodeList


def insert_hisData():
    for code in codeList:
        time.sleep(0.15)
        if code == '' or code is None:
            continue
        else:
            code_str = code
            if code_str[0:2] == "00" or code_str[0:2] == "30":
                code_str = code_str + ".SZ"
            else:
                code_str = code_str + ".SH"
            pro = ts.pro_api()
            df = pro.daily(ts_code=code_str, start_date=datetime.datetime.now().strftime('%Y%m%d'), end_date=datetime.datetime.now().strftime('%Y%m%d'))
            print(df)
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
                    print(json.loads(df1.to_json('records')))
                    db.indexdaily.insert(json.loads(df1.to_json('records')))
                except Exception:
                    print(df1['code'])


client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.test8
codeList = getcodeList()

insert_hisData()
