#!/bin/python3
# -*- coding:utf-8 -*-
import sys

import psycopg2

conn = psycopg2.connect(database="test", user="test1", password="gbase;123", host="192.168.100.100", port="15400")
cur = conn.cursor()
sql = 'select * from test1;'
cur.execute(sql)
rows = cur.fetchall()

for row in rows:
    print(row)

sys.exit()