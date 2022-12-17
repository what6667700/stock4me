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
import datetime
import time

ts.set_token('82214039a3bfd40645b630b18a46151509f4a4bbde00dbbd60ee3585')


def getcodeList():
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.test8
    stockCodeList = []
    for item in db.indexCode.find():
        code = item.get('CODE')
        # if code not in stockCodeList:
        stockCodeList.append(code)
    return stockCodeList


def insert_hisData(codeList):
    for code in codeList:
        time.sleep(0.5)
        if code == '' or code is None:
            continue
        else:
            # code_str = code
            # if code_str[0:2] == "00" or code_str[0:2] == "30":
            #     code_str = code_str + ".SZ"
            # else:
            #     code_str = code_str + ".SH"
            pro = ts.pro_api()
            # df = pro.daily(ts_code=code_str, start_date=datetime.datetime.now().strftime('%Y%m%d'), end_date=datetime.datetime.now().strftime('%Y%m%d'))
            # df1 = pro.index_daily(ts_code=code, start_date='20220124', end_date='20220201')


            df1 = pro.index_daily(ts_code=code, start_date=datetime.datetime.now().strftime('%Y%m%d'),end_date=datetime.datetime.now().strftime('%Y%m%d'))
            # df1 = pro.index_daily(ts_code=code, start_date='20221024',end_date='20221025')


            try:
                print(json.loads(df1.to_json(orient='records')))
                db.indexCodeData.insert(json.loads(df1.to_json(orient='records')))
                #db.historytradeInfo4Code.insert(json.loads(df1.to_json(orient='records')))
            except Exception:
                print(df1)
                # print(df1['ts_code'])
                continue


client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.test8
codeList = getcodeList()
insert_hisData(codeList)
