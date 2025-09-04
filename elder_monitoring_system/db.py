# db.py
import sqlite3
def save_log(event_type, file_path):
    conn = sqlite3.connect("activity_log.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (event TEXT, path TEXT, time TEXT)''')
    cursor.execute("INSERT INTO logs VALUES (?, ?, datetime('now'))", (event_type, file_path))
    conn.commit()
    conn.close()
