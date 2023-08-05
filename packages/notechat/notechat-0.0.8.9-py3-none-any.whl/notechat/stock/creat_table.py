#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/03 01:11
# @Author  : niuliangtao
# @Site    : 
# @File    : creat_table.py
# @Software: PyCharm

import pymysql.cursors
import tushare as ts

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='stock',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def create_stock_basic():
    try:
        with connection.cursor() as cursor:
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

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            sql = 'INSERT INTO stock_basic (ts_code,symbol) VALUES (%s, %s)'
            fields = "ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"
            param2 = ('%s, ' * len(fields.split(',')))[:-2]
            sql = 'INSERT INTO stock_basic ({}) VALUES ({})'.format(fields, param2)

            pro = ts.pro_api()
            fields = "ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"
            data = pro.stock_basic(exchange='', list_status='L', fields=fields)
            print(data)

            for line in data.values:
                cursor.execute(sql, tuple(line))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id, password FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
