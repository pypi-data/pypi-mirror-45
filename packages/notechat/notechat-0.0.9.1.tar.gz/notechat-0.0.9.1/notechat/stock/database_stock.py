#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/04 00:31
# @Author  : niuliangtao
# @Site    : 
# @File    : mysql.py
# @Software: PyCharm

import pymysql.cursors
import tushare as ts


class database_stock:
    def __init__(self):
        self.pro = ts.pro_api()
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='123456',
                                          db='stock',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def stock_basic_create(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = """CREATE TABLE IF NOT EXISTS stock_basic (
            id            INT(11)    NOT NULL AUTO_INCREMENT
           ,ts_code       VARCHAR(255) COMMENT 'TS代码'
           ,symbol        VARCHAR(255) COMMENT '股票代码'
           ,name          VARCHAR(255) COMMENT '股票名称'
           ,area          VARCHAR(255) COMMENT '所在地域'
           ,industry      VARCHAR(255) COMMENT '所属行业'
           ,fullname      VARCHAR(255) COMMENT '股票全称'
           ,enname        VARCHAR(255) COMMENT '英文全称'
           ,market        VARCHAR(255) COMMENT '市场类型 （主板/中小板/创业板）'
           ,exchange      VARCHAR(255) COMMENT '交易所代码'
           ,curr_type     VARCHAR(255) COMMENT '交易货币'
           ,list_status   VARCHAR(255) COMMENT '上市状态： L上市 D退市 P暂停上市'
           ,list_date     VARCHAR(255) COMMENT '上市日期'
           ,delist_date   VARCHAR(255) COMMENT '退市日期'
           ,is_hs         VARCHAR(255) COMMENT '是否沪深港通标的，N否 H沪股通 S深股通'

           ,PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;
        	"""
                cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)

    def stock_basic_init_data(self):
        try:
            with self.connection.cursor() as cursor:
                fields = "ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"
                param2 = ('%s, ' * len(fields.split(',')))[:-2]
                sql = 'INSERT INTO stock_basic ({}) VALUES ({})'.format(fields, param2)

                pro = ts.pro_api()
                fields = "ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"
                data = pro.stock_basic(exchange='', list_status='L', fields=fields)

                for line in data.values:
                    cursor.execute(sql, tuple(line))

            self.connection.commit()
        except Exception as e:
            print(e)

    def stock_basic_updated_data(self):
        try:
            with self.connection.cursor() as cursor:
                f = "ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"

                data = self.pro.stock_basic(exchange='', list_status='L', fields=f)

                for line in data.values:
                    fields = f.split(',')
                    values = line

                    equals = ""
                    wheres = "{}=\"{}\"".format(fields[0], values[0])
                    for i in range(1, len(fields)):
                        equals += "{}=\"{}\",".format(fields[i], values[i])

                    equals = equals[:-1]
                    sql = """UPDATE stock_basic SET {} WHERE {};""".format(equals, wheres)

                    cursor.execute(sql)

            self.connection.commit()
        except Exception as e:
            print(e)

    def stock_daily_create(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = """CREATE TABLE IF NOT EXISTS stock_daily (
               id            INT(11)    NOT NULL AUTO_INCREMENT
              ,ts_code       VARCHAR(255) COMMENT 'TS代码'
              ,trade_time    VARCHAR(255) COMMENT '交易时间'
              ,open          FLOAT        COMMENT '开盘价'
              ,high          FLOAT        COMMENT '最高价'
              ,low           FLOAT        COMMENT '最低价'
              ,close         FLOAT        COMMENT '收盘价'
              ,vol           FLOAT        COMMENT '成交量（手）'
              ,amount        FLOAT        COMMENT '成交额（千元）'
              ,trade_date    VARCHAR(255) COMMENT '交易日期'
              ,pre_close     FLOAT        COMMENT '昨收价'
              ,PRIMARY KEY (`id`)
           ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;
           	"""
                # ['ts_code', 'trade_time', 'open', 'high', 'low', 'close', 'vol', 'amount', 'trade_date', 'pre_close']
                cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)

    def stock_daily_init_data(self):
        try:
            with self.connection.cursor() as cursor:
                fields = "ts_code,trade_time,open,high,low,close,vol,amount,trade_date,pre_close"
                param2 = ('%s, ' * len(fields.split(',')))[:-2]
                sql = 'INSERT INTO stock_daily ({}) VALUES ({})'.format(fields, param2)

                pro = ts.pro_api()
                data = ts.pro_bar(api=pro, ts_code='000001.SH', asset='E', freq='5min', start_date='20150101',
                                  end_date='20190405')
                data = data.fillna(0)
                for line in data.values:
                    cursor.execute(sql, tuple(line))

            self.connection.commit()
        except Exception as e:
            print(e)


df = database_stock()

# df.stock_basic_create()
# df.stock_basic_init_data()
# df.stock_basic_updated_data()

df.stock_daily_create()
df.stock_daily_init_data()
