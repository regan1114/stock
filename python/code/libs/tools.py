# 產生從 startYear 年 startMonth 月到 endYear 年 endMonth 月的所有年與月的tuple
def createYearMonth(startYear, startMonth, endMonth, endYear): 
    start = 12 * startYear + startMonth
    end = 12 * endYear + endMonth
    for num in range(int(start), int(end) + 1):
        y, m = divmod(num, 12)
        yield y, m

def check_no_chinese(check_str):
    flag = False
    for ch in check_str:
        if u'\u4e00' >= ch or ch >= u'\u9fff':
            flag = True
    return flag

def check_float(value):
    try:
        number = float(value)
        return True
    except ValueError:
        return False

def isNaN(string):
    return string != string or string == 'nan'
