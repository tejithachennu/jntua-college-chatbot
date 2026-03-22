"""
admin_ui.py
Admin panel: upload files, build KB, manage data, view analytics.
"""

import streamlit as st
import os
import shutil
import pandas as pd
import plotly.express as px
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import KB_DIR, FAISS_DIR
from core.ingestor import ingest_all
from core.embedder import build_index, index_exists
from database.analytics import get_analytics
from database.db import init_db, get_conn


def show_admin():
    st.markdown("### ⚙️ Admin Panel")
    tab1, tab2, tab3 = st.tabs(["📂 Knowledge Base", "📊 Analytics", "📋 Query Logs"])

    # ── TAB 1: Knowledge Base Management ──────────────────────────────
    with tab1:
        st.subheader("Current Knowledge Base Files")
        files = os.listdir(KB_DIR)
        if files:
            for f in files:
                col1, col2 = st.columns([4, 1])
                col1.write(f"📄 {f}")
                if col2.button("Delete", key=f"del_{f}"):
                    os.remove(os.path.join(KB_DIR, f))
                    st.success(f"Deleted {f}")
                    st.rerun()
        else:
            st.info("No files in knowledge base yet.")

        st.divider()
        st.subheader("Upload New Files")
        uploaded = st.file_uploader(
            "Upload PDF, CSV, or TXT files",
            type=["pdf", "csv", "txt"],
            accept_multiple_files=True
        )
        if uploaded:
            for uf in uploaded:
                dest = os.path.join(KB_DIR, uf.name)
                with open(dest, "wb") as f:
                    f.write(uf.read())
            st.success(f"✅ {len(uploaded)} file(s) uploaded successfully.")

        st.divider()
        st.subheader("Build / Rebuild Knowledge Base")
        include_web = st.checkbox("Include JNTUA website scraping", value=True)
        st.caption("⚠️ Website scraping takes 2–5 minutes. Uncheck to build faster from files only.")

        if st.button("🔨 Build Knowledge Base", type="primary"):
            progress_bar = st.progress(0)
            status = st.empty()

            def update(msg, pct):
                status.write(msg)
                progress_bar.progress(pct)

            with st.spinner("Building knowledge base..."):
                chunks = ingest_all(include_website=include_web, progress_callback=update)
                update("Building FAISS index...", 0.9)
                build_index(chunks, progress_callback=update)

            st.success(f"✅ Knowledge base built with {len(chunks)} chunks!")
            st.balloons()

        if index_exists():
            st.info("✅ Knowledge base is ready.")
            if st.button("🗑️ Delete Index (force rebuild next time)"):
                shutil.rmtree(FAISS_DIR)
                os.makedirs(FAISS_DIR, exist_ok=True)
                st.warning("Index deleted. Please rebuild.")
                st.rerun()

    # ── TAB 2: Analytics Dashboard ─────────────────────────────────────
    with tab2:
        st.subheader("Usage Analytics")
        data = get_analytics()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Queries", data["total_queries"])
        m2.metric("Success Rate", f"{data['success_rate']}%")
        m3.metric("Fallback Rate", f"{data['fallback_rate']}%")
        m4.metric("Avg Confidence", data["avg_confidence"])

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top Intents**")
            if data["intent_counts"]:
                df_intent = pd.DataFrame(
                    data["intent_counts"].items(), columns=["Intent", "Count"]
                ).sort_values("Count", ascending=False)
                fig = px.bar(df_intent, x="Intent", y="Count", color="Intent",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(showlegend=False, margin=dict(t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")

        with col2:
            st.markdown("**Sentiment Distribution**")
            if data["sentiment_counts"]:
                df_sent = pd.DataFrame(
                    data["sentiment_counts"].items(), columns=["Sentiment", "Count"]
                )
                fig2 = px.pie(df_sent, names="Sentiment", values="Count",
                              color_discrete_sequence=px.colors.qualitative.Set3)
                fig2.update_layout(margin=dict(t=20, b=20))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No data yet.")

        st.markdown("**Language Distribution**")
        if data["lang_counts"]:
            df_lang = pd.DataFrame(
                data["lang_counts"].items(), columns=["Language", "Count"]
            )
            fig3 = px.bar(df_lang, x="Language", y="Count",
                          color_discrete_sequence=["#7F77DD"])
            fig3.update_layout(margin=dict(t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)

    # ── TAB 3: Query Logs ─────────────────────────────────────────────
    with tab3:
        st.subheader("Recent Query Logs")
        data = get_analytics()
        if not data["recent_df"].empty:
            df = data["recent_df"].copy()
            df["is_success"] = df["is_success"].map({1: "✅ Success", 0: "❌ Fallback"})
            st.dataframe(df, use_container_width=True, height=400)

            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Logs CSV", csv, "query_logs.csv", "text/csv")
        else:
            st.info("No queries logged yet.")

        st.divider()
        if st.button("🗑️ Clear All Logs"):
            conn = get_conn()
            conn.execute("DELETE FROM query_logs")
            conn.commit()
            conn.close()
            st.success("All logs cleared.")
            st.rerun()
