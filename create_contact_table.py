import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("تم إنشاء جدول contact_messages بنجاح.")
