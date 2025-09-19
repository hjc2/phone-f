import sqlite3
from pprint import pprint

### talked with Keith Alan Crabb about it being a sqlite3 db

# my program works by first viewing the "settings.db" file and finding the phone number in the "device_phone_number" field
# this is the phone number of the sender
# the "mmssms.db" file is the db of the messages sent by the work phone
# I search for every unique message sent by the phone, and record the quantity of messages sent
# the message "File has been uploaded to the server" appears only once, which is quite abnormal
# I grabbed the row and the details of the message, including the receiver
# I suspect this is where the data leak occured
# This also happended at roughly 3am in central time (Chicago)

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

def count_sms_bodies():
    conn = sqlite3.connect("mmssms.db")
    cursor = conn.cursor()
    
    # Count # of occurences for each body
    cursor.execute(f"SELECT body, COUNT(*) as count FROM sms WHERE body IS NOT NULL AND body != '' GROUP BY body ORDER BY count DESC, body")
    body_counts = cursor.fetchall()
    conn.close()

    return(body_counts)

def get_upload_message_row(message):
    conn = sqlite3.connect("mmssms.db")
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM sms WHERE body = '{message}'")
    row = cursor.fetchone()
    
    if row:
        # Get column names
        cursor.execute("PRAGMA table_info(sms)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Create dict of column:value pairs
        row_dict = dict(zip(columns, row))
        conn.close()
        return row_dict



db_data = get_settings()
print("Device Phone #")
print(db_data['global']['device_phone_number'])
print("Count of message body's")
quantities = count_sms_bodies()
print(quantities)
rarest_message = min(quantities, key=lambda x: x[1])
print(f"least common: {rarest_message}")
print("\n" + ("=" * 10) + "\n")
print(rarest_message[0])
uploaded = get_upload_message_row(rarest_message[0])
receiver = uploaded['address']

sender = db_data['global']['device_phone_number']
print(f"sender: {sender}")
print(f"receiver: {receiver}")

with open("colemanh_proj1_Answers.txt", "w") as f:
    f.write(f"sender: {sender}\n")
    f.write(f"receiver: {receiver}\n")

#print time
#print address
#export to new file
