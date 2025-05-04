import sqlite3

# Connect to SQLite (creates the DB if it doesn't exist)
conn = sqlite3.connect('cinderella_mystery.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    gender TEXT,
    age INTEGER,
    occupation TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS event_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    event_name TEXT,
    timestamp TEXT,
    dress_color TEXT,
    FOREIGN KEY (person_id) REFERENCES people(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lost_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    owner_id INTEGER,
    location TEXT,
    found_time TEXT,
    FOREIGN KEY (owner_id) REFERENCES people(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT,
    sent_time TEXT,
    FOREIGN KEY (sender_id) REFERENCES people(id),
    FOREIGN KEY (receiver_id) REFERENCES people(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS travel_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    from_location TEXT,
    to_location TEXT,
    travel_time TEXT,
    FOREIGN KEY (person_id) REFERENCES people(id)
);
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully.")