"""
sentiment.py
Simple rule-based sentiment detection.
Labels: positive, neutral, negative, frustrated
"""

NEGATIVE_WORDS = ["bad", "worst", "terrible", "useless", "wrong", "hate", "stupid", "not working",
                  "doesn't work", "failed", "failure", "disappointed", "frustrat", "angry", "upset",
                  "problem", "issue", "error", "broken", "pathetic"]

POSITIVE_WORDS = ["good", "great", "excellent", "helpful", "thanks", "thank you", "awesome",
                  "wonderful", "perfect", "nice", "well done", "appreciate", "love"]

def detect_sentiment(text: str) -> str:
    t = text.lower()
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in t)
    pos_count = sum(1 for w in POSITIVE_WORDS if w in t)

    if neg_count >= 2:
        return "frustrated"
    elif neg_count == 1:
        return "negative"
    elif pos_count >= 1:
        return "positive"
    return "neutral"
