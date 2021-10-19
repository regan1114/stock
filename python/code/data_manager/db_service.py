from numpy import string_
import pymysql
from configparser import ConfigParser
import logging
import os
from pprint import pprint

class DbService:
    _instance = None
    global connect, cursor, database

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.getConfig()
        self.connection()

    def getConfig(self):
        cfg = ConfigParser()
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'db_config.ini'))
        cfg.read(path)
        self.database = cfg['DATABASE']

    def connection(self):  # 連線資料庫
        try:
            self.connect = pymysql.connect(host=self.database['MYSQL_HOST'], db=self.database['MYSQL_DB'], 
                                        user=self.database['MYSQL_USER'], password=self.database['MYSQL_PASS'],
                                        charset='utf8', use_unicode=True)
            self.cursor = self.connect.cursor()
        except Exception as e:
            logging.error('Fail to connection mysql {}'.format(str(e)))

    def insert_list(self, dataList: list, tableName):  # 擷取從year-month開始到目前為止的所有交易日資料
        for i in range(len(dataList)):  # 取出該月的每一天編號為stockno的股票資料
            item = dataList.loc[i]
            date = ('{:%Y-%m-%d}'.format(item['ts_date']))
            row = self.check_info_exist(item, tableName)
            if not row:  # 不在資料庫
                insertsql = "INSERT INTO %s (ts_date, ts_stockno, ts_shares, ts_amount, ts_open, ts_close, ts_high, ts_low, ts_diff, ts_turnover) \
                    VALUES ('%s', '%s', '%ld', '%ld', '%f', '%f', '%f', '%f', '%f', '%d')" % (tableName, date, str(item['ts_stockno']),
                                                                                              int(item['ts_shares']), int(
                                                                                                  item['ts_amount']), float(item['ts_open']),
                                                                                              float(item['ts_close']), float(
                                                                                                  item['ts_high']), float(item['ts_low']),
                                                                                              float(item['ts_diff']), int(item['ts_turnover']))  # 插入資料庫的SQL
                self.cursor.execute(insertsql)  # 插入資料庫
                self.connect.commit()  # 插入時需要呼叫commit，才會修改資料庫

    def check_info_exist(self, info, tableName):
        date = ('{:%Y-%m-%d}'.format(info['ts_date']))
        selectSql = "select * from %s where ts_date = '%s' and ts_stockno = '%s'" % (tableName, date, str(info['ts_stockno']))  # 查詢是否已經在資料庫的SQL
        row = self.query_one(selectSql)
        return row

    def check_stock_category_exist(self, stockno):
        selectSql = "select * from tw_category where tc_stockno = '%s'" % (str(stockno))  # 查詢是否已經在資料庫的SQL        
        return self.query_one(selectSql)

    def execute(self, insertSql):  # 插入資料
        self.cursor.execute(insertSql)  # 插入資料庫
        self.connect.commit()  # 插入時需要呼叫commit，才會修改資料庫

    def list_execute(self, insertSql, list):  # 插入資料, 陣列
        self.cursor.execute(insertSql, tuple(list))  # 插入資料庫
        self.connect.commit()  # 插入時需要呼叫commit，才會修改資料庫

    def query_one(self, selectSql):
        self.cursor.execute(selectSql)  # 執行查詢的SQL
        return self.cursor.fetchone()  # 如果有取出第一筆資料

    def query_all(self, selectSql):
        self.cursor.execute(selectSql)  # 執行查詢的SQL
        return self.cursor.fetchall()  # 如果有取出全部資料

    def close(self):  # 關閉資料庫
        self.connect.close()
