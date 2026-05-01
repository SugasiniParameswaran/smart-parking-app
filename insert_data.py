import sqlite3

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

# ---------------- INSERT ADMINS ----------------

admins = [
    ("Arun", "A001", "1234"),
    ("Priya", "A002", "5678")
]

for admin in admins:
    try:
        cursor.execute(
            "INSERT INTO admins (name, admin_id, password) VALUES (?, ?, ?)",
            admin
        )
    except:
        pass  # Avoid duplicate error if run multiple times


# ---------------- INSERT BLOCKS ----------------

blocks = [
    ("Block A", 20, 8, 12, 55),
    ("Block B", 20, 10, 10, 50),
    ("Block C", 20, 5, 15, 60),
    ("Block D", 20, 5, 15, 60),
    ("Block E", 20, 8, 12, 55)
]

for block in blocks:
    try:
        cursor.execute(
            "INSERT INTO blocks (block_name, total_slots, free_slots, occupied_slots, price_per_hour) VALUES (?, ?, ?, ?, ?)",
            block
        )
    except:
        pass
    # ---------------- INSERT SLOTS ----------------

for block in blocks:
    block_name = block[0]
    total_slots = block[1]
    free_slots = block[2]

    for i in range(1, total_slots + 1):
        if i <= free_slots:
            status = "F"
        else:
            status = "O"

        try:
            cursor.execute(
                "INSERT INTO slots (block_name, slot_number, status) VALUES (?, ?, ?)",
                (block_name, i, status)
            )
        except:
            pass


conn.commit()
conn.close()

print("Sample admins and blocks inserted successfully.")
