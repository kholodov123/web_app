import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", password="111", host="127.0.0.1")
cursor = conn.cursor()

conn.autocommit = True
sql = "CREATE DATABASE web_app"

cursor.execute(sql)
print("DB CREATE SUCCSESSFULL")

cursor.close()
conn.close()