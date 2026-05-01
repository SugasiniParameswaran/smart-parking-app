import sqlite3

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM slots")
count = cursor.fetchone()[0]

print("Total slots in database:", count)

conn.close()
