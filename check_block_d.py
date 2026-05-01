import sqlite3

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

cursor.execute("""
SELECT slot_number, status 
FROM slots 
WHERE block_name = 'Block D'
ORDER BY slot_number
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
