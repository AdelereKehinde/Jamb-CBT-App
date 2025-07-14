import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("SELECT subject, question FROM questions")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

