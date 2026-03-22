import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KB_DIR = os.path.join(DATA_DIR, "knowledge_base")
FAISS_DIR = os.path.join(DATA_DIR, "faiss_index")
DB_PATH = os.path.join(DATA_DIR, "chatbot_logs.db")

# RAG settings
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 4
EMBED_MODEL = "all-MiniLM-L6-v2"

# LLM — using Groq (free). Replace with "openai" if preferred.
LLM_PROVIDER = "groq"          # "groq" or "openai"
GROQ_MODEL = "llama3-8b-8192"
OPENAI_MODEL = "gpt-3.5-turbo"

# College website to scrape
COLLEGE_WEBSITE = "https://www.jntua.ac.in"
SCRAPE_MAX_PAGES = 60          # Limit to avoid overload

# Languages supported
LANGUAGES = {"English": "en", "Telugu": "te"}

# Confidence threshold — below this = fallback response
CONFIDENCE_THRESHOLD = 0.35

# App
APP_TITLE = "JNTUA College Chatbot"
APP_ICON = "🎓"
