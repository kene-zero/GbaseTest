import psycopg2

conn = psycopg2.connect(database="postgres", user="test1", password="gbase;123", host="192.168.100.100", port="15400")
cur = conn.cursor()
cur.execute("""SELECT * from name_age;""")
rows = cur.fetchall()

for row in rows:
    print(row)

