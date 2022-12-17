# -*- coding: utf-8 -*-
import json
import random
import urllib3
import datetime
from bs4 import BeautifulSoup

from pymongo import MongoClient

from src import addData

client = MongoClient('mongodb://127.0.0.1:27017/')
mydb = client["test8"]
mycol = mydb["stockCode"]

url = 'http://quotes.money.163.com/old/#query=EQA&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0'

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
    # request = urllib.request.Request(url)
    # request.add_header('User-Agent', agent)
    # request.add_header('Host', 'quotes.money.163.com')
    # request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    return response.data.decode()


def getUrl(qquery, page=0, count=10000):
    # print(qquery)
    codeUrl = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=' + '%d' % page + '&query=' + qquery + '&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=' + '%d' % count + '&type=query'
    # print(type(codeUrl))
    return codeUrl


def getDataUrl(code, start=20170703, end=20170704):
    dataUrl = 'http://quotes.money.163.com/service/chddata.html?code=' + code + '&start=' + '%d' % start + '&end=' + '%d' % end + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    return dataUrl





str = getRequest(url)

# str = response.read().decode('utf-8')

bs = BeautifulSoup(str,features="lxml")

def getAllCode():
    for i in range(0, 4):
        result = bs.find('li', id='f0-f3-f' + '%d' % i)
        if result:
            qquery = result.get("qquery")
            if qquery != None:
                codeUrl = getUrl(qquery)
                data = getRequest(codeUrl)
                json_str = json.loads(data)
                list = json_str.get('list')
                if list:
                    for j in list:
                        code = j.get('CODE')
                        news_codes = []
                        code_codition ={
                            'CODE': code
                        }
                        select_count = mycol.count_documents(code_codition)

                        if select_count != 0:
                            for data in mycol.find():
                                data_codes = data.get('CODE')
                                news_codes.append(data_codes)
                        if code not in news_codes:
                            stockCode = {
                                'NAME': j.get('NAME'),
                                'CODE': j.get('CODE'),
                                'SYMBOL': j.get('SYMBOL'),
                                'CLOSE': j.get('CLOSE'),  # 收盘价
                                'HIGHESTPRICE': j.get('HIGHESTPRICE'),  # 最高价
                                'LOWESTPRICE': j.get('LOWESTPRICE'),  # 最低价
                                'OPEN': j.get('OPEN'),  # 开盘价
                                'PREVIOUSCLOSE': j.get('PREVIOUSCLOSE'),  # 前收盘
                                'UPDOWN': j.get('UPDOWN'),  # 涨跌额
                                'PERCENT': j.get('PERCENT'),  # 涨跌幅
                                'HS': j.get('HS'),  # 换手率
                                'VOLUME': j.get('VOLUME'),  # VOLUME
                                'TURNOVER': j.get('TURNOVER'),  # 成交金额
                                'PE': j.get('PE'),  # 市盈率
                                'MCAP': j.get('MCAP'),  # 流通市值
                                'TCAP': j.get('TCAP'),  # 总市值
                                'MFSUM': j.get('MFSUM'),  # 每股收益
                                'MFRATIO2': j.get('MFRATIO').get('MFRATIO2'),  # 净利润
                                'MFRATIO10': j.get('MFRATIO').get('MFRATIO10')  # 主营收
                            }
                            mycol.insert_one(stockCode)


if __name__ == '__main__':
    getAllCode()
    begin = datetime.datetime.now().strftime('%Y%m%d')
    end = datetime.datetime.now().strftime('%Y%m%d')
    addData.updateDate(begin, end)
