import re
from numpy.testing._private.utils import print_assert_equal
import requests
from bs4 import BeautifulSoup
import pandas
from datetime import datetime ,date
import json
import sys
import numpy as np
import time
from imp import reload
from data_manager import db_service
from libs import tools

# 未上市上櫃公開發行 strMode=1
# 上市 strMode=2
# 上市上櫃債券 strMode=3
# 上櫃 strMode=4
# 興櫃 strMode=5
# 期貨及選擇權 strMode=6
# 開放式證券投資信託基金 strMode=7
# 未公開發行之創櫃板證券 strMode=8
# 買賣黃金現貨 strMode=9
# 外幣計價可轉換定期存單 strMode=10
def get_stock_list(number):
    try:
        respStockList = requests.get(
            "http://isin.twse.com.tw/isin/C_public.jsp?strMode=%s" % (number))
        dataFrame = pandas.read_html(respStockList.text)[0]        
        dataFrame = dataFrame.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
        
        dataList = []
        for i in range(len(dataFrame)):
            value = dataFrame.iloc[i][0][0]
            if tools.check_no_chinese(value):
                dataList.append(sort_column_data(dataFrame.iloc[i]))
        return dataList
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

def sort_column_data(column):
    data = []
    for i in range(len(column)):
        index = 0
        value = column[i]
        splitValue = []
        if not tools.check_float(value) or not tools.isNaN(value):
            removeSpaceString = value.lstrip().rstrip()
            split = removeSpaceString.split()
            
            if len(split) > 2:
                string = ''
                for j in range(1, len(split)):
                    string += split[j] + ' '
                splitValue.append(split[0])
                splitValue.append(string)
            else :
                splitValue = split    
        elif tools.check_float(value):
            splitValue = [value]
        elif tools.isNaN(value):
            splitValue.append('')

        for j in range(len(splitValue)):
            newValue = splitValue[j]
            data.append(newValue)
            index += 1
    return data

def update():
    #更新當下日期字串
    today = date.today() 
    dataString = today.strftime("%Y-%m-%d")
    
    results = []
    #取上市個股資訊
    tempList = get_stock_list(2)
    for item in tempList:
        if (item[6].find('ESV') == 0) or (item[6].find('CEO') == 0):
            item.append('')
            item.append(dataString)
            results.append(item)
    
    time.sleep(2)

    otc_stock_list =[]
    #取上櫃個股資訊
    tempList = get_stock_list(4) 
    for item in tempList:
        if (item[6].find('ESV') == 0) or (item[6].find('CEO') == 0):
            otc_stock_list.append(item[0])
            item.append('')
            item.append(dataString)
            results.append(item)
    
    # time.sleep(2)
    # #取興櫃個股資訊
    # tempList = get_stock_list(5)
    # for item in tempList:
    #     if (item[6].find('ESV') == 0):
    #         item.append('')
    #         item.append(dataString)
    #         results.append(item)
    
    dataTable = pandas.DataFrame(results)
    dataTable.columns = ['tc_stockno', 'tc_name', 'tc_isin_code', 'tc_publicdate',
                    'tc_market', 'tc_industry', 'tc_cfi_code', 'tc_note', 'tc_update_date', 'tc_modify_date']
    
    insert_stock_info(dataTable)
    delete_expired_otc(otc_stock_list)

#將整理好的資訊寫入資料庫中
def insert_stock_info(dataTable):     
    dbService = db_service.DbService()

    for i in range(len(dataTable)):  # 取出該月的每一天編號為stockno的股票資料
        item = dataTable.loc[i]
        stockno = item['tc_stockno']
        actionSql = ''
        if not dbService.check_stock_category_exist(stockno):
            actionSql = "INSERT INTO tw_category (tc_publicdate, tc_stockno, tc_name, tc_isin_code, tc_market, tc_industry, tc_cfi_code, tc_note, tc_modify_date) \
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (str(item['tc_publicdate']), str(item['tc_stockno']), str(item['tc_name']),
                                                                                            str(item['tc_isin_code']), str(item['tc_market']), str(item['tc_industry']),
                                                                                            str(item['tc_cfi_code']), str(item['tc_note']), str(item['tc_modify_date']))  # 插入資料庫的SQL            
        else:
            actionSql = "UPDATE tw_category SET tc_modify_date = '%s' WHERE tc_stockno = '%s'" %(str(item['tc_modify_date']), str(item['tc_stockno']))
        dbService.execute(actionSql)

def query_all(category=''):
    dbService = db_service.DbService()
    sqlStr = ' SELECT * FROM tw_category'
    if len(category) != 0:
        sqlStr += " WHERE tc_market = '%s'" % (category)
    sqlStr += ' ORDER BY tc_stockno'
    dataTable = dbService.query_all(sqlStr)
    return dataTable

def get_list(category=''):
    results = query_all(category)
    dataTable = pandas.DataFrame(results)
    dataTable.columns = ['tc_id', 'tc_publicdate', 'tc_enddate', 'tc_stockno', 'tc_name', 'tc_isin_code',
                         'tc_interest_rate', 'tc_market', 'tc_industry', 'tc_cfi_code', 'tc_note', 'tc_update_date', 'tc_modify_date']    
    return dataTable

def update_date(date, stockNo):
    dbService = db_service.DbService()
    actionSql = "UPDATE tw_category SET tc_update_date = '%s' WHERE tc_stockno = '%s'" %(date, stockNo)
    dbService.execute(actionSql)

#刪除已下市的股票
def delete_expired_otc(stock_list):
    dbService = db_service.DbService()
    format_strings = ','.join(['%s'] * len(stock_list))
    actionSql = "DELETE FROM tw_category WHERE tc_market = '上櫃' AND tc_stockno NOT IN (%s)" % format_strings
    dbService.list_execute(actionSql, stock_list)