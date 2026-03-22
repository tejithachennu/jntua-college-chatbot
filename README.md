# 🎓 JNTUA College Information Chatbot

> AI-powered chatbot for JNTUA College of Engineering, Anantapur  
> **Team PathFinders** | Tejitha Chennu (24001A0550) | Chandana Manni (24001A0554)

---

## 🚀 Features

| Feature | Status |
|---|---|
| Natural language Q&A | ✅ |
| Telugu language support | ✅ |
| Multi-turn conversations | ✅ |
| PDF / CSV / Website ingestion | ✅ |
| Google Gemini 2.0 AI | ✅ |
| Campus map + navigation | ✅ |
| Sentiment detection | ✅ |
| Intent classification | ✅ |
| Admin panel + analytics | ✅ |
| Query logs + dashboard | ✅ |
| 80%+ accuracy evaluation | ✅ |

---

## 🏗️ Architecture
```
User Query → Language Detection → Translation (if Telugu)
→ FAISS Vector Search → Top-6 Chunks Retrieved
→ Gemini 2.0 Flash → Clean Answer → Translate Back
→ Display with Source Reference
```

---

## 📁 Project Structure
```
college_chatbot/
├── main.py                  # Entry point — run this
├── config.py                # All settings
├── requirements.txt         # Dependencies
├── .env                     # API keys (not uploaded)
├── app/
│   ├── chat_ui.py           # Chat interface + map
│   └── admin_ui.py          # Admin panel
├── core/
│   ├── ingestor.py          # PDF/CSV/Web scraper
│   ├── embedder.py          # FAISS index builder
│   ├── retriever.py         # Vector search
│   ├── llm_chain.py         # Gemini answer generation
│   ├── translator.py        # English ↔ Telugu
│   ├── intent.py            # Intent classifier
│   └── sentiment.py         # Sentiment detector
├── database/
│   ├── db.py                # SQLite setup
│   ├── logger.py            # Query logging
│   └── analytics.py         # Dashboard metrics
└── tests/
    ├── eval.py              # Accuracy evaluation
    └── test_dataset.csv     # 15 test questions
```

---

## ⚡ Quick Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install google-genai

# 2. Add Gemini API key to .env
GEMINI_API_KEY=your_key_here

# 3. Run the app
streamlit run main.py
```

Get free Gemini API key at: https://aistudio.google.com

---

## 🧪 Run Accuracy Test
```bash
python tests/eval.py
```

Target: ≥ 80% correct responses on 15 test cases.

---

## 🏫 About

**JNTUA College of Engineering, Anantapur**  
Andhra Pradesh, India  
Website: www.jntua.ac.in  
Anti-Ragging Helpline: 9000551425  
Principal: 9440796804

---

## 🛠️ Tech Stack

Python • Streamlit • Google Gemini 2.0 Flash • FAISS • sentence-transformers • PyMuPDF • SQLite • BeautifulSoup • deep-translator