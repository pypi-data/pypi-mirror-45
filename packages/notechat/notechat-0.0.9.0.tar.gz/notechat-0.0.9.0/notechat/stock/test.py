import tushare as ts

ts.set_token('79b91762c7f42780ccd697e5d228f28b446fb13a938e5012a2c1d25e')
pro = ts.pro_api()

df = ts.pro_bar(api=pro, ts_code='000001.SH', asset='E', freq='5min', start_date='20180101', end_date='20181011')

print(df)


def stock_daily_create(self):
    try:
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = """CREATE TABLE IF NOT EXISTS stock_basic (
           id            INT(11)    NOT NULL AUTO_INCREMENT
          ,ts_code       VARCHAR(255) COMMENT 'TS代码'
          ,trade_date    VARCHAR(255) COMMENT '交易日期'
          ,open          FLOAT        COMMENT '开盘价'
          ,high          FLOAT        COMMENT '最高价'
          ,low           FLOAT        COMMENT '最低价'
          ,close         FLOAT        COMMENT '收盘价'
          ,pre_close     FLOAT        COMMENT '昨收价'
          ,change        FLOAT        COMMENT '涨跌额'
          ,pct_chg       FLOAT        COMMENT '涨跌幅（未复权，如果是复权请用 通用行情接口 ）'
          ,vol           FLOAT        COMMENT '成交量（手）'
          ,amount        FLOAT        COMMENT '成交额（千元）'

          ,PRIMARY KEY (`id`)
       ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;
       	"""
            cursor.execute(sql)
        self.connection.commit()
    except Exception as e:
        print(e)
