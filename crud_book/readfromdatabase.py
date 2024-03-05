import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()

cursor.execute("select * from books")

rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the cursor and the connection
cursor.close()
conn.close()