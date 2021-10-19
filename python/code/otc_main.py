# !/usr/bin/python
# coding:utf-8

import sys
from datetime import date, datetime
import time
from tw_stocks import otc_service, category_service
from data_manager import db_service
from libs import settings
import calendar

#預設起始時間、股價更新時間、上市發行日
searchType = ['StartDate', 'UpdateDate', 'publicDate']

def update_price():
    dbService = db_service.DbService()
    parameters = settings.get_parameter('OtcUpdateTime')
    parameter = parameters.loc[0]
    updateDate = datetime.strptime(parameter['value'], "%Y-%m-%d").date()
    
    today = date.today()
    # 預設資料起始日期
    startTime = datetime.strptime('2010-01-01',"%Y-%m-%d").date()
    # dataTable = tw_category.get_list('上櫃')
    # item = dataTable.loc[0]

    searchDate = startTime 

    if updateDate > startTime:
        searchDate = updateDate
    
    if(updateDate >= today):
        return

    newUpdateDate = ''
    
    for year in range(searchDate.year, (today.year + 1)):
        RocYear = year - 1911
        endMonth = 12 
        if year == today.year:
            endMonth = today.month
        
        for month in range(searchDate.month, endMonth + 1):
            endDay = calendar.monthrange(year, month)[1]
            endDay = today.day if (year == today.year and month == today.month) else endDay
            startDay = 1
            if (searchDate.year == year and searchDate.month == month):
                startDay = searchDate.day
            for day in range(startDay, endDay + 1):
                getDate = str(RocYear) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2)
                results = otc_service.get_data(getDate)
                
                isBlock = False
                if results is None:
                    isBlock = True
                    while isBlock:
                        blockTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print("block time:", blockTime)
                        time.sleep(1800)
                        print('blocking.....')
                        results = otc_service.get_data(getDate)
                        if results is not None:
                            print('重新抓到資料')
                            isBlock = False
                            dbService = db_service.DbService()
                        else:
                            print('無法抓資料')

                if len(results) > 0:
                    dbService.insert_list(results, 'tw_otc_stock')
                    newUpdateDate = '%s-%s-%s' %(str(year), str(month).zfill(2), str(day).zfill(2))
                    
    if(len(newUpdateDate) > 0):
        settings.update_parameter(newUpdateDate, 'OtcUpdateTime')
        otc_service.delete_expired_otc_info()

if __name__ == '__main__':
    # tw_category.update()
    update_price()
    
    
