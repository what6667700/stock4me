# -*- coding: utf-8 -*-

import random
import urllib3
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.test8
mycol = db['stock']


def getRequest(url):
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    ]
    agent = random.choice(user_agents)
    http = urllib3.PoolManager(num_pools=5, headers={'User-Agent':agent,'Host':'quotes.money.163.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})

    response = http.request('GET', url)
    return response.data.decode(encoding='GBK',errors='ignore')

def getDataUrl(code, start, end):
    dataUrl = 'http://quotes.money.163.com/service/chddata.html?code=' + code + '&start=' +  start + '&end=' + end + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    return dataUrl

def day_get():
    date = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    day = date - oneday
    date_from = datetime.datetime(day.year, day.month, day.day)
    return date_from.strftime("%Y%m%d")


def getStockCodeDataUrl(code):
    #start = time.strftime('%Y%m%d', time.localtime(time.time()))
    #end = time.strftime('%Y%m%d', time.localtime(time.time()))
    # start=day_get()
    end=day_get()
    # dataUrl = 'http://quotes.money.163.com/service/chddata.html?code=' + code + '&start=' + start + '&end=' + end + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    dataUrl = 'http://quotes.money.163.com/service/chddata.html?code=' + code + '&end=' + end + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    return dataUrl

def insertStockInfo():
    timeOutCodes=[]
    count=0
    for codes in db.stockCode.find():
        dataUrl = getStockCodeDataUrl(codes.get('CODE'))
        print(dataUrl)
        try:
            resultR = getRequest(dataUrl)
        except Exception as e:
            timeOutCodes.append(codes)
            print(str(e))
        arr = resultR.split('\r\n')
        for p in range(1, (len(arr) - 1)):
            gupiao = arr[p].split(",")
            stock = {
                'TIME': gupiao[0].replace("-",""),
                "CODE": gupiao[1].split("\'")[1],
                "NAME": gupiao[2],
                "CLOSE": float(gupiao[3]) if gupiao[3] != "None" else None,
                "HIGHESTPRICE": float(gupiao[4]) if gupiao[4] != "None" else None,
                "LOWESTPRICE": float(gupiao[5]) if gupiao[5] != "None" else None,
                "OPEN": float(gupiao[6]) if gupiao[6] != "None" else None,
                "PREVIOUSCLOSE": float(gupiao[7]) if gupiao[7] != "None" else None,
                "UPDOWN": float(gupiao[8]) if gupiao[8] != "None" else None,
                "PERCENT": float(gupiao[9]) if gupiao[9] != "None" else None,
                "HS": float(gupiao[10]) if gupiao[10] != "None" else None,
                "VOLUME": float(gupiao[11]) if gupiao[11] != "None" else None,
                "TURNOVER": float(gupiao[12]) if gupiao[12] != "None" else None,
                "TCAP": float(gupiao[13]) if gupiao[13] != "None" else None,
                "MCAP": float(gupiao[14]) if gupiao[14] != "None" else None
            }
            # db.stock.insert_one({"TIME": datetime.datetime.strptime(gupiao[0], '%Y-%m-%d'), "CODE": gupiao[1].split("\'")[1].encode('utf-8')}, {"$setOnInsert": stock})
            # print(stock)
            mycol.insert_one(stock)
            # print(stock)
    print(count)
    if timeOutCodes:
        print(timeOutCodes)

if __name__ == '__main__':
    # date = datetime.datetime.now().strftime('%Y%m%d')
    insertStockInfo()
