from logging import error
import numpy as np
import requests
import pandas
from libs import tools
from datetime import datetime
import numpy.ma as ma
from data_manager import db_service
    
#   https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d=107/02/09  取107/02/09當天的股價與成交量
def stock_info(date):
    try:
        url = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d=%s' % (date)
        print(url)
        r = requests.get(url, timeout = 5)
        data = r.json()
         # 進行資料格式轉換
        return transform(data) if len(data['aaData']) else []
    except:
        # sys.exit("上櫃 URL 有誤，可能斷線或被擋")  
        # print("上櫃 URL 有誤，可能斷線或block")
        return None

def transform_date(date):
    y, m, d = date.split('/')
    return str(int(y)+1911) + '/' + m + '/' + d  # 民國轉西元

def transform_data(data, date):
    info = [0] * 10
    info[0] = date
    info[1] = data[0]
    info[2] = int(data[8].replace(',', ''))  # 把千進位的逗點去除
    info[3] = int(data[9].replace(',', ''))
    info[4] = float(0.0 if '--' in data[4].replace(',', '') else data[4].replace(',', ''))
    info[5] = float(0.0 if '--' in data[5].replace(',', '') else data[5].replace(',', ''))
    info[6] = float(0.0 if '--' in data[6].replace(',', '') else data[6].replace(',', ''))
    info[7] = float(0.0 if '--' in data[2].replace(',', '') else data[2].replace(',', ''))
    if ('--' in data[3].replace(',', '')) or ('除權' in data[3].replace(',', '') or ('除息' in data[3].replace(',', ''))):# +/-/X表示漲/跌/不比價
        info[8] = float(0.0)
    else:
        info[8] = float(data[3].replace(',', ''))
    info[9] = int(data[10].replace(',', ''))
    return info

def transform(data):
    date = datetime.strptime(transform_date(data['reportDate']), '%Y/%m/%d')
    dataList = []
    for d in data['aaData']:
        if len(d[0]) == 4:
            info = transform_data(d,date)
            dataList.append(info)
    return dataList

def get_data(date):
    list = stock_info(date)
    if list is None:
        return None
    if(len(list) == 0):
        return []
    s = pandas.DataFrame(list)
    s.columns = ['ts_date','ts_stockno', 'ts_shares', 'ts_amount', 'ts_open',
                 'ts_high', 'ts_low', 'ts_close', 'ts_diff', 
                 'ts_turnover']
    # "日期","股票代碼","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"
    return s

def delete_expired_otc_info():
    dbService = db_service.DbService()
    actionSql = " DELETE FROM tw_otc_stock "
    actionSql += "WHERE ts_stockno NOT IN ("
    actionSql += "    SELECT tc_stockno FROM tw_category WHERE tc_market = '上櫃'"
    actionSql += ")"
    dbService.execute(actionSql)
    