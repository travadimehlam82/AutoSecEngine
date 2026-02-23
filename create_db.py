import sqlite3

conn = sqlite3.connect("events.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS events")

c.execute("""
CREATE TABLE events (
    timestamp TEXT,
    event_type TEXT,
    file_path TEXT,
    details TEXT
)
""")

conn.commit()
conn.close()

print("Database table created successfully")
