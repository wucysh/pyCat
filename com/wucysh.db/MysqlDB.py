#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
MYSQL 数据库操作
"""
import MySQLdb
import pandas.io.sqlas sql
conn = MySQLdb.connect(host = 'xx.xx.xx.xx', user = 'xx', 
        passwd= 'xx', db= 'xx', port = x, charset = 'utf8')
data = sql.read_frame(‘select * from xxx’, conn)
print(data)
conn.close()