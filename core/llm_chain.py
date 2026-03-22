import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONFIDENCE_THRESHOLD

FALLBACK_RESPONSE = "I'm sorry, I don't have that info. Please visit www.jntua.ac.in or call 9440796804."

PROMPT = """You are a helpful assistant for JNTUA College of Engineering, Anantapur.
RULES:
- Answer ONLY from the context below
- Give SHORT, CLEAN, DIRECT answers
- Never dump raw text — always give a neat answer
- Use bullet points for lists
- If context does not have the answer say: I don't have that info. Please visit www.jntua.ac.in

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

def _get_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    if key and len(key) > 20:
        return key
    for path in [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        r"C:\college_chatbot\college_chatbot\.env",
    ]:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        key = line.strip().split("=", 1)[1].strip()
                        if len(key) > 20:
                            os.environ["GEMINI_API_KEY"] = key
                            return key
    return ""

def generate_answer(query, chunks, confidence, history=None):
    if confidence < CONFIDENCE_THRESHOLD or not chunks:
        return FALLBACK_RESPONSE, False
    context = "\n\n".join([f"[{i+1}] {c['text']}" for i, c in enumerate(chunks)])
    prompt = PROMPT.format(context=context, question=query)
    key = _get_key()
    if not key:
        print("[LLM] No key found")
        return chunks[0]["text"][:400], True
    try:
        from google import genai
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        answer = response.text.strip()
        print(f"[LLM] Gemini OK: {answer[:60]}")
        return answer, True
    except Exception as e:
        print(f"[LLM] Error: {e}")
        return chunks[0]["text"][:400], True