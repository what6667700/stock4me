# coding=utf-8
# 开始计算。以平安银行为例：
# !/usr/local/bin/python
# -*- coding: utf-8 -*-

import math
import pandas as pd
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import tushare as ts
import datetime
import stockstats
import pymongo
import json
import baostock as bs
import pandas as pd
import time

print(ts.__version__)
# 30abde40af1725d6670ea349b624e31bbf8a50022c25de8ec9da4f53 -
# 82214039a3bfd40645b630b18a46151509f4a4bbde00dbbd60ee3585 - Gary
ts.set_token('82214039a3bfd40645b630b18a46151509f4a4bbde00dbbd60ee3585')


def get_kdj_by_stock_code(begin_time, end_time, stock_code):
    code_str = stock_code
    # code_str = str(stock_code, encoding="utf8")
    if code_str[0:3] == "000" or code_str[0:3] == "002" or code_str[0:3] == "300":
        code_str = code_str + ".SZ"
    else:
        code_str = code_str + ".SH"

    print(code_str)
    # stock = ts.get_hist_data(code_str, start=begin_time, end=end_time)
    # time.sleep(0.005)
    pro = ts.pro_api()
    stock = pro.daily(ts_code=code_str, start_date=begin_time, end_date=end_time)

    # stock = getBaoStock(begin_time,end_time,code_str)
    if stock is None:
        print()
    else:
        #print(stock["trade_date"])
        # stock["datep"] = stock.index.values #增加日期列。
        # stock["trade_date"] = stock.index.values
        stock = stock.sort_index(0, ascending=False)  # 将数据按照日期排序下。
        # stock['stockcode']=code_str
        # stockStat = stockstats.StockDataFrame.retype(stock,code_str)
        stockStat = stockstats.StockDataFrame.retype(stock)
        # stock['rsi'] = stockStat['rsi_14']
        # KDJ, default to 9 days
        # stock['kdjk'] = stockStat['kdjk']
        # stock['kdjd'] = stockStat['kdjd']
        # stock['kdjj'] = stockStat['kdjj']
        # MACD
        # stock['macd'] = stockStat['macd']
        # MACD signal line
        # stock['macds'] = stockStat['macds']
        # MACD histogram
        # stock['macdh'] = stockStat['macdh']

        # bolling, including upper band and lower band
        # stock['boll'] = stockStat['boll']
        # stock['boll_ub'] = stockStat['boll_ub']
        # stock['boll_lb'] = stockStat['boll_lb']
        # print(stock)

        # print(type(stockStat))
        # print(len(stockStat))
        if len(stockStat) > 0:
            # df1 = stockStat[['open','high','close','low','volume','price_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20','p_change','stockcode','kdjk','kdjd','kdjj','macd','macds','macdh','boll','boll_ub','boll_lb','dma','rsi_6','rsi_12','cci','cci_20','datep']]

            df1 = stockStat[
                ['ts_code', 'trade_date', 'open', 'high', 'close', 'low', 'vol', 'pct_chg', 'kdjk', 'kdjd', 'kdjj',
                 'macd', 'macds', 'macdh', 'boll', 'boll_ub', 'boll_lb']]
            # print(stockStat)
            dftransform = df1.fillna(value=0)
            db.stkdj.insert(json.loads(dftransform.T.to_json()).values())
    # print(type(stockStat[['stockcode', 'kdjk', 'kdjd', 'kdjj']]))
    # db.cftest.insert(json.loads(stockStat.to_json(orient='records')))
    # print("init finish .")
    # print(stockStat[['stockcode', 'kdjk', 'kdjd', 'kdjj']])


def getBaoStock(begin_time, end_time, stock_code):
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    rs = bs.query_history_k_data_plus(stock_code,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=begin_time, end_date=end_time,
                                      frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 登出系统 ####
    bs.logout()
    return result


def getcodeList():
    stockCodeList = []
    for item in db.stockCode.find():
        # print item.get('SYMBOL')
        code = item.get('SYMBOL')
        if code not in stockCodeList:
            stockCodeList.append(code)
    return stockCodeList


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient['test8']


def get_kdj():
    # print 123
    db.stkdj.drop();
    startdate = '19901201'
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    # 获取截至上一个交易日的历史行情
    predate = today - delta
    # print(predate)
    strpredate = datetime.datetime.strftime(today, '%Y%m%d')
    stock_list = getcodeList()
    for code in stock_list:
        # code_str = str(code, encoding="utf8")


        # code_str = code
        # if code_str[0:2] == "00" or code_str[0:2] == "30":
        #     code_str = code_str + ".SZ"
        # else:
        #     code_str = code_str + ".SH"
        #
        # search_set = db.stkdj
        # if search_set.find_one({"ts_code":code_str}) == None:
           get_kdj_by_stock_code(startdate, strpredate, code)
        # else:
        #    continue


           # print(code+" exits!!!")

    # db.stkdj.remove({"boll_ub": None})Å
    # db.stkdj.remove({"cci": None})
    # db.stkdj.remove({"cci_20": None})
    # db.stkdj.remove({"rsi_6": None})
    # db.stkdj.remove({"rsi_12": None})


def jobIndex():
    get_kdj()
    # print("adf")

jobIndex()
#
# scheduler = BlockingScheduler()
# scheduler.add_job(jobIndex, "cron", day_of_week="1-5", hour=17, minute=40, misfire_grace_time=3600)
# scheduler.start()