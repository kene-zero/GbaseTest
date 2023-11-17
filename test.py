import psycopg2

conn = psycopg2.connect(database="postgres", user="test1", password="gbase;123", host="192.168.100.100", port="15400")
cur = conn.cursor()
cur.execute("""SELECT tablerows('"' ||table_schema || '"."' || table_name || '"') AS CT,
table_schema || '.' || table_name 
AS table_full_name
FROM 
information_schema.tables
where table_catalog='ecology_2210'
ORDER BY
    tablerows('"' ||table_schema || '"."' || table_name || '"')
DESC ;""")
rows = cur.fetchall()

for row in rows:
    print(row)




