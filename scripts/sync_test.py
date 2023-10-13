import psycopg2
from psycopg2 import extras

database = 'postgres'
user = 'test'
password = ''
table_name = ''
host = ''
port = ''
insert_data = ()

conn = psycopg2.connect(database='postgres', user=user, password=password, host='', port='')
cursor = conn.cursor()
sql = f"insert into {table_name} values %s"
data_list = []
for x in range(100000):
    data_list.append(insert_data)
