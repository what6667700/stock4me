# coding=utf-8

import tushare as ts
from pymongo import MongoClient
import json
import time
import datetime
import stockstats


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
        time.sleep(0.1)
        if code == '' or code is None:
            continue
        else:
            # code = str(code, "utf8")
            if code[0:2] == "00" or code[0:3] == "30":
                code = code + ".SZ"
            else:
                code = code + ".SH"
            pro = ts.pro_api()

            fmt = '%Y%m%d'
            begin = datetime.datetime.now().strftime('%Y%m%d')
            end = datetime.datetime.now().strftime('%Y%m%d')
            # begin = datetime.date(2022, 6, 24)
            # end = datetime.date(2022, 6, 24)
            for i in range((end - begin).days + 1):
                time.sleep(1)
                day = begin + datetime.timedelta(days=i)
                dailystr = day.strftime(fmt)
                df = pro.daily_basic(ts_code=code, trade_date=dailystr,fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
                print(type(df))
                try:
                    df1 = df.reset_index()
                    db.dailyBasicPro.insert(json.loads(df1.to_json(orient='records')))
                except Exception:
                    print(df)


insert_hisData()


# 名称	类型	描述
# ts_code	str	TS股票代码
# trade_date	str	交易日期
# close	float	当日收盘价
# turnover_rate	float	换手率（%）
# turnover_rate_f	float	换手率（自由流通股）
# volume_ratio	float	量比
# pe	float	市盈率（总市值/净利润， 亏损的PE为空）
# pe_ttm	float	市盈率（TTM，亏损的PE为空）
# pb	float	市净率（总市值/净资产）
# ps	float	市销率
# ps_ttm	float	市销率（TTM）
# dv_ratio	float	股息率 （%）
# dv_ttm	float	股息率（TTM）（%）
# total_share	float	总股本 （万股）
# float_share	float	流通股本 （万股）
# free_share	float	自由流通股本 （万）
# total_mv	float	总市值 （万元）
# circ_mv	float	流通市值（万元）
