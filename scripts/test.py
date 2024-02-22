#!/bin/python3
# -*- coding:utf-8 -*-

import sys
import psycopg2

conn = psycopg2.connect(database="test", user="test1", password="gbase;123", host="192.168.100.100", port="15400")
cur = conn.cursor()
cur.execute('create table python_test(id int,name varchar);')
print(cur.statusmessage)

cur.execute("select * from python_test;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute('insert into python_test values(1),(2),(3);')
print(cur.statusmessage)

cur.execute("select * from python_test;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("delete from python_test where id=3")
print(cur.statusmessage)

cur.execute("select * from python_test;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("update python_test set name='kane' where id=1")
print(cur.statusmessage)

cur.execute("select * from python_test;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("drop table python_test")
print(cur.statusmessage)
