import sqlite3

def db_to_simple_dict(db_file):
    # GRAB DATA FROM SETTINGS
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    db_dict = {}

    for table in cursor.fetchall():
        cursor.execute(f"SELECT * FROM {table[0]}")
        db_dict[table[0]] = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return db_dict

# Usage
db_data = db_to_simple_dict("settings.db")
print(db_data)

print(db_data['global']['device_phone_number'])