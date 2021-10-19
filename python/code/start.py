# !/usr/bin/python
# coding:utf-8

from datetime import date, datetime
import time
from libs import settings
import listed_main, otc_main
from tw_stocks import category_service

if __name__ == '__main__':
    startTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("schedule start time :", startTime)
    scheduleStatus = settings.get_schedule_status()
    if(scheduleStatus == "0" ):
        # 啟動任務
        settings.update_parameter('1','DailySchedule')
        startTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("individual stocks infomation update start time:", startTime)
        # 更新個股資訊
        category_service.update()
        endTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("end time:", endTime)
        # 更新上市股價    
        listed_main.update_price()
        # 更新上櫃股價
        otc_main.update_price()
        # 更新狀態
        settings.update_parameter('0','DailySchedule')
    else:
        print("implement the schedule")
