"""
db.py
SQLite setup — creates tables for query logging and analytics.
"""

import sqlite3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
            query       TEXT NOT NULL,
            answer      TEXT,
            intent      TEXT,
            sentiment   TEXT,
            language    TEXT,
            confidence  REAL,
            is_success  INTEGER DEFAULT 1,
            source_docs TEXT
        )
    """)
    conn.commit()
    conn.close()
