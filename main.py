import sqlite3

# GRAB DATA FROM SETTINGS
def get_settings():
    conn = sqlite3.connect("settings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    db_dict = {}

    for table in cursor.fetchall():
        cursor.execute(f"SELECT * FROM {table[0]}")
        db_dict[table[0]] = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return db_dict

def count_messages():

# Usage
db_data = get_settings()
# print(db_data)

print("Device Phone #")
print(db_data['global']['device_phone_number'])

