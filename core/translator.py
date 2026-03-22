"""
translator.py
Detects language and translates between English and Telugu.
Uses deep-translator (free, no API key needed).
"""

from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException


def detect_language(text: str) -> str:
    """Returns ISO language code: 'en', 'te', etc."""
    try:
        return detect(text)
    except LangDetectException:
        return "en"


def translate_to_english(text: str) -> tuple[str, str]:
    """
    Translate text to English if needed.
    Returns (translated_text, original_lang_code).
    """
    lang = detect_language(text)
    if lang == "en":
        return text, "en"
    try:
        translated = GoogleTranslator(source=lang, target="en").translate(text)
        return translated, lang
    except Exception as e:
        print(f"[Translator] to-EN error: {e}")
        return text, lang


def translate_to_telugu(text: str) -> str:
    """Translate English text to Telugu."""
    try:
        return GoogleTranslator(source="en", target="te").translate(text)
    except Exception as e:
        print(f"[Translator] to-TE error: {e}")
        return text


def translate_answer(answer: str, target_lang: str) -> str:
    """Translate the final answer to target language if not English."""
    if target_lang == "en":
        return answer
    try:
        return GoogleTranslator(source="en", target=target_lang).translate(answer)
    except Exception as e:
        print(f"[Translator] answer translation error: {e}")
        return answer
