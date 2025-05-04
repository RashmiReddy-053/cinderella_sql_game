import sqlite3

conn = sqlite3.connect('cinderella_mystery.db')
cursor = conn.cursor()

# People
people = [
    ("Ella", "Female", 22, "Florist"),         # Cinderella 💙
    ("Beatrice", "Female", 24, "Chef"),
    ("Diana", "Female", 21, "Teacher"),
    ("Leo", "Male", 25, "Prince"),             # The hero 👑
    ("Charles", "Male", 30, "Knight")
]
cursor.executemany("INSERT INTO people (name, gender, age, occupation) VALUES (?, ?, ?, ?);", people)

# Fetch IDs for easy reference
cursor.execute("SELECT id, name FROM people")
people_map = {name: pid for pid, name in cursor.fetchall()}

# Event Attendance
attendance = [
    (people_map["Ella"], "Grand Royal Ball", "2024-02-14 22:30", "blue"),  # before midnight
    (people_map["Beatrice"], "Grand Royal Ball", "2024-02-14 23:30", "red"),
    (people_map["Diana"], "Grand Royal Ball", "2024-02-14 23:50", "blue"),
    (people_map["Leo"], "Grand Royal Ball", "2024-02-14 21:00", "black")
]
cursor.executemany("INSERT INTO event_attendance (person_id, event_name, timestamp, dress_color) VALUES (?, ?, ?, ?);", attendance)

# Lost Item (glass slipper!)
lost_items = [
    ("glass slipper", people_map["Ella"], "Palace Ballroom", "2024-02-14 23:55"),
    ("earring", people_map["Diana"], "Palace Garden", "2024-02-14 23:59")
]
cursor.executemany("INSERT INTO lost_items (item_name, owner_id, location, found_time) VALUES (?, ?, ?, ?);", lost_items)

# Messages
messages = [
    (people_map["Ella"], people_map["Leo"], "Thank you for the dance. Maybe we'll meet again.", "2024-02-14 23:50"),
    (people_map["Diana"], people_map["Charles"], "I saw you near the garden.", "2024-02-14 23:52")
]
cursor.executemany("INSERT INTO messages (sender_id, receiver_id, message, sent_time) VALUES (?, ?, ?, ?);", messages)

# Travel logs (Cinderella came from a nearby village)
travel_logs = [
    (people_map["Ella"], "Rosewood Village", "Royal City", "2024-02-14 18:00"),
    (people_map["Beatrice"], "Royal City", "Royal City", "2024-02-14 19:00"),
    (people_map["Diana"], "Royal City", "Royal City", "2024-02-14 19:30")
]
cursor.executemany("INSERT INTO travel_logs (person_id, from_location, to_location, travel_time) VALUES (?, ?, ?, ?);", travel_logs)

conn.commit()
conn.close()

print("Sample data inserted successfully.")
