from logging import error
import sys
import numpy as np
import requests
import pandas
from libs import tools
from datetime import datetime

#   http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20180817&stockNo=2330  取一個月的股價與成交量

def stock_info(date, stock_no):
    try:
        url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % (
            date, stock_no)
        print(url)
        r = requests.get(url, timeout = 5)
        data = r.json()
        if(data['stat'] != 'OK'):
            return []
        return transform(data['data'])  # 進行資料格式轉換
    except:
        # sys.exit("上市 URL 有誤，可能斷線或block") 
        # print("上市 URL 有誤，可能斷線或block")
        return None

def transform_date(date):
    y, m, d = date.split('/')
    return str(int(y)+1911) + '/' + m + '/' + d  # 民國轉西元

def transform_data(data):
    data[0] = datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    data[1] = int(data[1].replace(',', ''))  # 把千進位的逗點去除
    data[2] = int(data[2].replace(',', ''))
    data[3] = float(0.0 if data[3].replace(',', '') == '--' else data[3].replace(',', ''))
    data[4] = float(0.0 if data[4].replace(',', '') == '--' else data[4].replace(',', ''))
    data[5] = float(0.0 if data[5].replace(',', '') == '--' else data[5].replace(',', ''))
    data[6] = float(0.0 if data[6].replace(',', '') == '--' else data[6].replace(',', ''))
    data[7] = float(0.0 if data[7].replace(',', '') ==
                    'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
    data[8] = int(data[8].replace(',', ''))
    return data

def transform(data):
    return [transform_data(d) for d in data]

def get_data(date, stock_no):
    info = stock_info(date, stock_no)
    if info is None:
        return None
    if(len(info) == 0):
        return []
    s = pandas.DataFrame(info)
    s.columns = ['ts_date', 'ts_shares', 'ts_amount', 'ts_open',
                 'ts_high', 'ts_low', 'ts_close', 'ts_diff', 
                 'ts_turnover']
    # "日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"
    stock = []
    for i in range(len(s)):
        stock.append(stock_no)
    # 新增股票代碼欄，之後所有股票進入資料表才能知道是哪一張股票
    s['ts_stockno'] = pandas.Series(stock, index=s.index)
    return s
