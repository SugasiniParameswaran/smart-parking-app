import sqlite3

# Connect to database (will create file automatically)
conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

# ------------------ ADMIN TABLE ------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    admin_id TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# ------------------ DRIVER TABLE ------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    vehicle_number TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

# ------------------ BLOCK TABLE ------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_name TEXT UNIQUE NOT NULL,
    total_slots INTEGER NOT NULL,
    free_slots INTEGER NOT NULL,
    occupied_slots INTEGER NOT NULL,
    price_per_hour INTEGER NOT NULL
)
""")
# ------------------ SLOTS TABLE ------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_name TEXT NOT NULL,
    slot_number INTEGER NOT NULL,
    status TEXT NOT NULL
)
""")


conn.commit()
conn.close()

print("Database and tables created successfully.")
