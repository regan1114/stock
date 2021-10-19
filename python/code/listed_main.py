# !/usr/bin/python
# coding:utf-8

import sys
from datetime import date, datetime
import time
import pandas
from tw_stocks import listed_service, category_service
from data_manager import db_service
import calendar
from pprint import pprint

#預設起始時間、股價更新時間、上市發行日
searchType = ['StartDate', 'UpdateDate', 'publicDate']

def update_price():
    dbService = db_service.DbService()
    today = date.today()
    # 預設資料起始日期
    startTime = datetime.strptime('2010-01-01',"%Y-%m-%d").date()
    dataTable = category_service.get_list('上市')
    
    for i in range(len(dataTable)):
        item = dataTable.loc[i]
        
        enumType = 0

        updateDate = item['tc_update_date']
        publicDate = item['tc_publicdate']
        # modifyDate = item['tc_modify_date']
        #更新日是否大於起始日期，更新日預設:1900-01-01
        searchDate = startTime 
        if updateDate > startTime:
            searchDate = updateDate
            enumType = 1

        #股票上市日是否於查詢日期
        if publicDate > searchDate: 
            searchDate = publicDate
            enumType = 2
        
        if(today >= updateDate):
            for year in range(searchDate.year, (today.year + 1)):
                #如果是今年，則以現在月份為主
                endMonth = 12 
                if year == today.year:
                    endMonth = today.month
                isContinue = False
                startMontn = 1
                if enumType == 1 and year == updateDate.year:
                    startMontn = updateDate.month
                    if updateDate.day >= today.day and updateDate.month > today.month and updateDate.year == today.year:
                        isContinue = True
                    
                elif enumType == 2 and year == publicDate.year:
                    startMontn = publicDate.month

                if isContinue :
                    continue

                #從一月開始撈資料
                for month in range(startMontn, (endMonth + 1)):
                    #取得當月最後一天，當查詢日
                    day = calendar.monthrange(year, month)[1]
                    #如果是現在的月份，查詢日則以今日為主
                    day = today.day if (year == today.year and month == today.month) else day
                    originDate = datetime(year,month,day).date()
                    dateString = str(originDate)
                    getDate = dateString.replace('-', '')
                    result = listed_service.get_data(getDate, item['tc_stockno'])
                    isBlock = False
                    if result is None:
                        isBlock = True
                        while isBlock:
                            blockTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            print("block time:", blockTime)
                            time.sleep(1800)
                            print('blocking.....')
                            result = listed_service.get_data(getDate, item['tc_stockno'])
                            if result is not None:
                                print('重新抓到資料')
                                isBlock = False
                                dbService = db_service.DbService()
                            else:
                                print('無法抓資料')
                    if len(result) > 0:
                        #寫入上市股票資料
                        # print(result)
                        dbService.insert_list(result, 'tw_listed_stock')
                    category_service.update_date(originDate, item['tc_stockno'])
                    #間隔秒數，避免被證交所擋，實測隔五秒以上才不被擋
                    time.sleep(5)

if __name__ == '__main__':
    # tw_category.update()
    update_price()
    
    
