import sqlite3
from typing import List, Tuple

DB_PATH = "localmind.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    con.commit()
    con.close()

def add_message(role: str, content: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO chats (role, content) VALUES (?, ?)", (role, content))
    con.commit()
    con.close()

def get_history(limit: int = 50) -> List[Tuple[int, str, str, str]]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, role, content, ts FROM chats ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    con.close()
    return rows

def clear_history():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM chats")
    con.commit()
    con.close()
