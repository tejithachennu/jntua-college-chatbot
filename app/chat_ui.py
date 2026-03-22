"""
chat_ui.py - Main chat interface with map support
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.retriever import retrieve
from core.llm_chain import generate_answer
from core.translator import translate_to_english, translate_answer, detect_language
from core.intent import classify_intent
from core.sentiment import detect_sentiment
from core.embedder import index_exists
from database.logger import log_query

SUGGESTED_QUESTIONS = [
    "When does B.Tech I Year instruction period start?",
    "What are the subjects in CSE department?",
    "Who is the anti-ragging committee chairman?",
    "What are the M.Tech programs offered?",
    "When is Mid Exam 1 for III Year B.Tech?",
    "Contact details of the principal?",
]

# Keywords that trigger map display
MAP_KEYWORDS = [
    "map", "location", "where is", "how to reach", "directions",
    "address", "navigate", "find college", "college location",
    "how to come", "route", "show map", "college map"
]

COLLEGE_LAT = 14.6819
COLLEGE_LON = 77.6006
COLLEGE_NAME = "JNTUA College of Engineering, Anantapur"


def is_map_request(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in MAP_KEYWORDS)


def show_map():
    """Display JNTUA college location map using Streamlit."""
    import pandas as pd

    st.markdown("📍 **JNTUA College of Engineering, Anantapur**")

    # Show map using streamlit's built-in map
    df = pd.DataFrame({
        "lat": [COLLEGE_LAT],
        "lon": [COLLEGE_LON]
    })
    st.map(df, zoom=15)

    # Also show Google Maps link
    gmaps_url = f"https://www.google.com/maps?q={COLLEGE_LAT},{COLLEGE_LON}"
    st.markdown(f"🗺️ [Open in Google Maps]({gmaps_url})")
    st.markdown("""
**Address:**
JNTUA College of Engineering
Anantapur - 515002
Andhra Pradesh, India

**How to reach:**
- 🚆 Anantapur Railway Station — 3 km
- ✈️ Bengaluru Airport — 200 km
- ✈️ Tirupati Airport — 180 km
- 🚌 APSRTC Bus Stand — 2 km
""")


def show_chat():
    st.markdown("### 🎓 JNTUA College Chatbot")
    st.caption("Ask anything about admissions, departments, exams, faculty, or facilities.")

    col1, col2 = st.columns([3, 1])
    with col2:
        lang_choice = st.selectbox("Language", ["English", "Telugu"], key="lang_select")
    ui_lang = "te" if lang_choice == "Telugu" else "en"

    if not index_exists():
        st.warning("⚠️ Knowledge base not built yet. Go to **Admin Panel** → click **Build Knowledge Base**.")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "raw_history" not in st.session_state:
        st.session_state.raw_history = []

    # Suggested questions
    if not st.session_state.chat_history:
        st.markdown("**Suggested questions:**")
        cols = st.columns(3)
        for i, q in enumerate(SUGGESTED_QUESTIONS):
            with cols[i % 3]:
                if st.button(q, key=f"sq_{i}", use_container_width=True):
                    st.session_state._pending_query = q

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg.get("is_map"):
                show_map()
            else:
                st.markdown(msg["content"])

    pending = st.session_state.pop("_pending_query", None)
    user_input = st.chat_input(
        "Type your question here..." if ui_lang == "en" else "మీ ప్రశ్న ఇక్కడ టైప్ చేయండి..."
    )
    query = pending or user_input

    if query:
        # Show user message
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.chat_history.append({"role": "user", "content": query})

        with st.chat_message("assistant"):

            # ── MAP REQUEST ──────────────────────────────────────
            if is_map_request(query):
                show_map()
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "map",
                    "is_map": True
                })
                log_query(
                    query=query, answer="[MAP SHOWN]",
                    intent="contact", sentiment="neutral",
                    language="en", confidence=1.0,
                    is_success=True, source_docs=["map"]
                )

            # ── NORMAL QUESTION ──────────────────────────────────
            else:
                with st.spinner("Thinking..."):
                    eng_query, src_lang = translate_to_english(query)
                    intent = classify_intent(eng_query)
                    sentiment = detect_sentiment(eng_query)
                    chunks, confidence = retrieve(eng_query)
                    answer_en, is_success = generate_answer(
                        eng_query, chunks, confidence,
                        history=st.session_state.raw_history
                    )
                    final_answer = translate_answer(answer_en, ui_lang)
                    sources = list(set(c.get("source", "") for c in chunks[:3]))
                    source_text = ""
                    if sources and is_success:
                        source_text = "\n\n---\n📚 *Sources: " + ", ".join(sources) + "*"

                    display_answer = final_answer + source_text
                    st.markdown(display_answer)

                    if sentiment == "frustrated":
                        st.info("😔 Having trouble? Call Anti-Ragging helpline: 9000551425")

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": display_answer,
                    "is_map": False
                })
                st.session_state.raw_history.append({"role": "user", "content": eng_query})
                st.session_state.raw_history.append({"role": "assistant", "content": answer_en})

                log_query(
                    query=query, answer=answer_en,
                    intent=intent, sentiment=sentiment,
                    language=src_lang, confidence=confidence,
                    is_success=is_success, source_docs=sources,
                )

    if st.session_state.chat_history:
        if st.button("🗑️ Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.session_state.raw_history = []
            st.rerun()