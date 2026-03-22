"""
main.py
Entry point for the JNTUA College Chatbot Streamlit app.
Run with: streamlit run main.py
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import APP_TITLE, APP_ICON
from database.db import init_db

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize DB on startup
init_db()

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    st.markdown("**JNTUA College of Engineering**  \nAnantapur, Andhra Pradesh")
    st.divider()
    page = st.radio(
        "Navigate",
        ["💬 Chat", "⚙️ Admin Panel"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("**Quick Links**")
    st.markdown("🌐 [JNTUA Website](https://www.jntua.ac.in)")
    st.markdown("📞 Anti-Ragging: 9000551425")
    st.markdown("📞 Principal: 9440796804")
    st.divider()
    st.caption("Powered by RAG + LangChain + FAISS")

# ── Page Routing ───────────────────────────────────────────────────────
if page == "💬 Chat":
    from app.chat_ui import show_chat
    show_chat()
else:
    from app.admin_ui import show_admin
    show_admin()
