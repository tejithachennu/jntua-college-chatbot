"""
analytics.py
Reads query_logs and returns metrics for the admin dashboard.
"""

import sqlite3
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_conn, init_db


def get_analytics() -> dict:
    init_db()
    conn = get_conn()
    try:
        df = pd.read_sql("SELECT * FROM query_logs ORDER BY timestamp DESC", conn)
    except Exception:
        return _empty_analytics()
    finally:
        conn.close()

    if df.empty:
        return _empty_analytics()

    total = len(df)
    success = df["is_success"].sum()
    fallback = total - success

    intent_counts = df["intent"].value_counts().to_dict()
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    lang_counts = df["language"].value_counts().to_dict()

    # Recent queries (last 50)
    recent = df[["timestamp", "query", "intent", "sentiment", "is_success"]].head(50)

    return {
        "total_queries": total,
        "success_count": int(success),
        "fallback_count": int(fallback),
        "success_rate": round((success / total) * 100, 1) if total else 0,
        "fallback_rate": round((fallback / total) * 100, 1) if total else 0,
        "intent_counts": intent_counts,
        "sentiment_counts": sentiment_counts,
        "lang_counts": lang_counts,
        "recent_df": recent,
        "avg_confidence": round(df["confidence"].mean(), 3) if total else 0,
    }


def _empty_analytics() -> dict:
    return {
        "total_queries": 0, "success_count": 0, "fallback_count": 0,
        "success_rate": 0, "fallback_rate": 0,
        "intent_counts": {}, "sentiment_counts": {}, "lang_counts": {},
        "recent_df": pd.DataFrame(), "avg_confidence": 0,
    }
