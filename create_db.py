import psycopg

conn = psycopg.connect(dbname='postgres', user='postgres', password='151310', host='localhost', port=5432)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT datname FROM pg_database WHERE datname = %s", ('AIVOA',))
row = cur.fetchone()
if row is None:
    cur.execute('CREATE DATABASE "AIVOA"')
    print('CREATED AIVOA')
else:
    print('EXISTS AIVOA')
cur.close()
conn.close()
