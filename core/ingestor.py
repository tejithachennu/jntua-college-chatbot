"""
ingestor.py
Reads all knowledge base sources and returns clean text chunks.
Sources: PDF, CSV, TXT (uploaded files) + website scraping (JNTUA)
"""

import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import fitz  # PyMuPDF
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import KB_DIR, CHUNK_SIZE, CHUNK_OVERLAP, COLLEGE_WEBSITE, SCRAPE_MAX_PAGES


def chunk_text(text: str, source: str) -> list[dict]:
    """Split text into overlapping chunks with metadata."""
    text = re.sub(r'\s+', ' ', text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if chunk.strip():
            chunks.append({"text": chunk.strip(), "source": source})
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def ingest_txt(filepath: str) -> list[dict]:
    """Read a plain text file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return chunk_text(text, source=os.path.basename(filepath))


def ingest_pdf(filepath: str) -> list[dict]:
    """Extract text from all pages of a PDF."""
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return chunk_text(full_text, source=os.path.basename(filepath))


def ingest_csv(filepath: str) -> list[dict]:
    """
    Convert CSV rows into natural language sentences for embedding.
    Handles academic_calendar.csv and anti_ragging.csv intelligently.
    """
    df = pd.read_csv(filepath, encoding="utf-8", skip_blank_lines=True).dropna(how="all")
    filename = os.path.basename(filepath)
    chunks = []

    if "academic_calendar" in filename.lower():
        # Forward-fill program/year/semester columns
        df.columns = [c.strip() for c in df.columns]
        df = df.ffill()
        for _, row in df.iterrows():
            try:
                text = (
                    f"{row.get('Program','')} {row.get('Year','')} "
                    f"{row.get('Semester','')}: {row.get('Event','')} "
                    f"from {row.get('From','')} to {row.get('To','')} "
                    f"(Duration: {row.get('Duration','')})."
                )
                chunks.append({"text": text.strip(), "source": filename})
            except Exception:
                continue

    elif "anti_ragging" in filename.lower() or "antiragging" in filename.lower():
        df.columns = [c.strip() for c in df.columns]
        for _, row in df.iterrows():
            try:
                text = (
                    f"Anti-Ragging Committee - {row.iloc[0]}: "
                    f"{row.iloc[1]} ({row.iloc[2]}), Contact: {row.iloc[3]}."
                )
                chunks.append({"text": text.strip(), "source": filename})
            except Exception:
                continue
    else:
        # Generic CSV: convert each row to sentence
        for _, row in df.iterrows():
            text = ", ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            if text.strip():
                chunks.append({"text": text.strip(), "source": filename})

    return chunks


def scrape_website(base_url: str, max_pages: int = SCRAPE_MAX_PAGES) -> list[dict]:
    """
    Crawl the college website starting from base_url.
    Visits up to max_pages internal links and extracts clean text.
    """
    visited = set()
    to_visit = [base_url]
    all_chunks = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; CollegeChatbot/1.0)"}
    base_domain = urlparse(base_url).netloc

    print(f"[Scraper] Starting crawl of {base_url} (max {max_pages} pages)...")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove nav, footer, scripts
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            text = re.sub(r'\s+', ' ', text).strip()

            if len(text) > 100:
                chunks = chunk_text(text, source=url)
                all_chunks.extend(chunks)
                print(f"[Scraper] Scraped: {url} ({len(chunks)} chunks)")

            # Collect internal links
            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"])
                parsed = urlparse(href)
                if parsed.netloc == base_domain and href not in visited:
                    if not any(href.endswith(ext) for ext in [".pdf", ".jpg", ".png", ".zip", ".doc"]):
                        to_visit.append(href)

            time.sleep(0.5)  # Be polite to server

        except Exception as e:
            print(f"[Scraper] Failed {url}: {e}")
            continue

    print(f"[Scraper] Done. Total pages scraped: {len(visited)}, chunks: {len(all_chunks)}")
    return all_chunks


def ingest_all(include_website: bool = True, progress_callback=None) -> list[dict]:
    """
    Master function: ingest all files in KB_DIR + scrape website.
    Returns list of {text, source} dicts.
    """
    all_chunks = []

    files = os.listdir(KB_DIR)
    total = len(files)

    for i, filename in enumerate(files):
        filepath = os.path.join(KB_DIR, filename)
        if progress_callback:
            progress_callback(f"Reading {filename}...", (i + 1) / (total + 1))
        try:
            if filename.endswith(".pdf"):
                all_chunks.extend(ingest_pdf(filepath))
            elif filename.endswith(".csv"):
                all_chunks.extend(ingest_csv(filepath))
            elif filename.endswith(".txt"):
                all_chunks.extend(ingest_txt(filepath))
        except Exception as e:
            print(f"[Ingestor] Error on {filename}: {e}")

    if include_website:
        if progress_callback:
            progress_callback("Scraping JNTUA website (this may take 2-3 mins)...", 0.8)
        web_chunks = scrape_website(COLLEGE_WEBSITE)
        all_chunks.extend(web_chunks)

    print(f"[Ingestor] Total chunks ready: {len(all_chunks)}")
    return all_chunks
