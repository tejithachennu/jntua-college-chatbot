"""
logger.py
Logs every chatbot interaction to SQLite.
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_conn, init_db


def log_query(
    query: str,
    answer: str,
    intent: str,
    sentiment: str,
    language: str,
    confidence: float,
    is_success: bool,
    source_docs: list[str]
):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO query_logs
        (query, answer, intent, sentiment, language, confidence, is_success, source_docs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        query, answer, intent, sentiment, language,
        round(confidence, 4), int(is_success),
        json.dumps(source_docs)
    ))
    conn.commit()
    conn.close()
