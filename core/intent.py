"""
intent.py
Classifies user query intent for analytics and routing.
Uses keyword matching — no external API needed.
"""

INTENT_MAP = {
    "admissions": ["admission", "apply", "application", "eligibility", "cutoff", "rank", "eamcet", "counselling", "fee", "fees", "tuition"],
    "academics": ["exam", "exams", "syllabus", "schedule", "timetable", "calendar", "semester", "results", "marks", "grade", "mid", "theory", "lab"],
    "departments": ["department", "civil", "eee", "mechanical", "ece", "cse", "mca", "mtech", "btech", "course", "program", "subjects"],
    "faculty": ["faculty", "professor", "hod", "head", "staff", "teacher", "lecturer", "principal"],
    "facilities": ["library", "hostel", "canteen", "lab", "wifi", "internet", "sports", "bus", "transport", "campus"],
    "anti_ragging": ["ragging", "anti-ragging", "committee", "complaint", "helpline"],
    "placements": ["placement", "job", "recruit", "company", "campus", "drive", "package", "salary"],
    "contact": ["contact", "phone", "email", "address", "location", "office", "reach"],
    "events": ["event", "fest", "cultural", "technical", "symposium", "workshop", "seminar"],
}

def classify_intent(query: str) -> str:
    q = query.lower()
    scores = {intent: 0 for intent in INTENT_MAP}
    for intent, keywords in INTENT_MAP.items():
        for kw in keywords:
            if kw in q:
                scores[intent] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"
