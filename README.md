# 🎓 JNTUA College Information Chatbot

AI-powered chatbot for JNTUA College of Engineering, Anantapur.
Built with Streamlit + LangChain + FAISS + RAG architecture.

---

## 📁 Project Structure

```
college_chatbot/
├── main.py                  # Entry point — run this
├── config.py                # All settings in one place
├── requirements.txt
├── .env                     # API keys (never commit this)
├── app/
│   ├── chat_ui.py           # Chat interface
│   └── admin_ui.py          # Admin panel
├── core/
│   ├── ingestor.py          # PDF / CSV / TXT / Web scraper
│   ├── embedder.py          # FAISS index builder
│   ├── retriever.py         # Vector search
│   ├── llm_chain.py         # LLM answer generation
│   ├── translator.py        # English ↔ Telugu
│   ├── intent.py            # Intent classifier
│   └── sentiment.py         # Sentiment detector
├── database/
│   ├── db.py                # SQLite setup
│   ├── logger.py            # Query logging
│   └── analytics.py         # Dashboard metrics
├── data/
│   ├── knowledge_base/      # Your uploaded files go here
│   └── faiss_index/         # Auto-generated index
└── tests/
    ├── eval.py              # Accuracy evaluation script
    └── test_dataset.csv     # Optional custom test cases
```

---

## ⚡ Quick Setup (5 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a FREE Groq API key
- Visit https://console.groq.com
- Sign up → Create API Key → Copy it

### 3. Add your API key
Edit `.env`:
```
GROQ_API_KEY=your_actual_key_here
```

### 4. Run the app
```bash
streamlit run main.py
```

### 5. Build the knowledge base
- Open the app in browser (http://localhost:8501)
- Go to **Admin Panel** → **Knowledge Base** tab
- Check/uncheck "Include website scraping"
- Click **Build Knowledge Base**
- Wait 2–5 minutes for scraping to complete

---

## 💬 Features

| Feature | Status |
|---|---|
| Natural language Q&A | ✅ |
| Telugu language support | ✅ |
| Multi-turn conversations | ✅ |
| PDF ingestion | ✅ |
| CSV ingestion | ✅ |
| Website scraping (JNTUA) | ✅ |
| Anti-hallucination prompt | ✅ |
| Intent classification | ✅ |
| Sentiment detection | ✅ |
| Admin panel | ✅ |
| Query logs + analytics | ✅ |
| Accuracy evaluation | ✅ |

---

## 🧪 Run Accuracy Evaluation
```bash
python tests/eval.py
```
Target: ≥ 80% correct responses on 15 built-in test cases.

---

## 📂 Adding More Knowledge

Place any of these in `data/knowledge_base/`:
- `.pdf` files (brochures, rulebooks, fee structure)
- `.csv` files (faculty list, timetable, hostel info)
- `.txt` files (department info, notices)

Then rebuild the knowledge base from Admin Panel.

---

## 🔧 Configuration

Edit `config.py` to change:
- `TOP_K` — how many chunks to retrieve (default: 4)
- `CHUNK_SIZE` — text chunk size (default: 300 chars)
- `SCRAPE_MAX_PAGES` — how many website pages to crawl (default: 60)
- `CONFIDENCE_THRESHOLD` — minimum score to give an answer (default: 0.35)
- `LLM_PROVIDER` — switch between `"groq"` (free) and `"openai"` (paid)

---

## 📞 College Quick Contacts

| Role | Contact |
|---|---|
| Principal | 9440796804 |
| Anti-Ragging Helpline | 9000551425 |
| JNTUA Website | www.jntua.ac.in |
