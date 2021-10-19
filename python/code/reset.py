# !/usr/bin/python
# coding:utf-8

from datetime import date, datetime
from libs import settings

if __name__ == '__main__':
    settings.update_parameter('0','DailySchedule')
    endTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("reset time: ", endTime)
    
