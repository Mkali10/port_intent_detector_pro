# backend/database.py
import sqlite3
from backend.utils import timestamp

DB_FILE = "connections_log.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pid INTEGER,
        process_name TEXT,
        exe_path TEXT,
        local_addr TEXT,
        remote_addr TEXT,
        protocol TEXT,
        intent TEXT,
        suspicious INTEGER,
        ts TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_connection(pid, process_name, exe_path, laddr, raddr, proto, intent, suspicious):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO connections
    (pid, process_name, exe_path, local_addr, remote_addr, protocol, intent, suspicious, ts)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (pid, process_name, exe_path, str(laddr), str(raddr), proto, intent, int(suspicious), timestamp()))
    conn.commit()
    conn.close()
