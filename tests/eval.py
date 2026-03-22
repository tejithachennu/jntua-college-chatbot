"""
eval.py
Evaluates chatbot accuracy on a test dataset.
Run: python tests/eval.py
Reports: total, correct, success rate, fallback rate
"""

import sys
import os
import csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.retriever import retrieve
from core.llm_chain import generate_answer, FALLBACK_RESPONSE
from core.embedder import index_exists

# Built-in test cases using your actual data
BUILTIN_TESTS = [
    {"question": "When does B.Tech I Year instruction period start?", "expected_keywords": ["25-08-2025", "August"]},
    {"question": "When is Mid Exam 1 for BTech II Year?", "expected_keywords": ["18-08-2025", "August"]},
    {"question": "What are the subjects in CSE?", "expected_keywords": ["Java", "DBMS", "Python", "OS"]},
    {"question": "What are subjects in ECE department?", "expected_keywords": ["Electronic", "Digital", "EMWaves"]},
    {"question": "When was civil department established?", "expected_keywords": ["1946"]},
    {"question": "Who is the Anti-Ragging Committee Chairman?", "expected_keywords": ["Inspector", "Police"]},
    {"question": "Contact number of principal?", "expected_keywords": ["9440796804"]},
    {"question": "When are BTech III Year lab exams?", "expected_keywords": ["01-11-2025", "November"]},
    {"question": "What programs does ECE offer?", "expected_keywords": ["DECS", "VLSI", "IoT", "UG", "PG"]},
    {"question": "When does MCA I instruction period end?", "expected_keywords": ["13-12-2025", "December"]},
    {"question": "What is the hostel in-charge contact for Ellora hostel?", "expected_keywords": ["9247192692", "Dilip"]},
    {"question": "What are mechanical engineering subjects?", "expected_keywords": ["Thermodynamics", "Manufacturing"]},
    {"question": "When is BTech IV Year Mid Exam 2?", "expected_keywords": ["29-10-2025", "October"]},
    {"question": "What specializations does Mechanical M.Tech offer?", "expected_keywords": ["Heat Power", "IC Engines", "Energy"]},
    {"question": "What does the Humanities department offer?", "expected_keywords": ["English", "Economics", "Commerce"]},
]


def run_eval(test_cases=None):
    if not index_exists():
        print("❌ Knowledge base not built. Run the admin panel → Build Knowledge Base first.")
        return

    cases = test_cases or BUILTIN_TESTS
    print(f"\n{'='*60}")
    print(f"  JNTUA Chatbot Accuracy Evaluation — {len(cases)} test cases")
    print(f"{'='*60}\n")

    correct = 0
    fallback_count = 0

    for i, tc in enumerate(cases, 1):
        question = tc["question"]
        expected_kws = tc.get("expected_keywords", [])

        chunks, confidence = retrieve(question)
        answer, is_success = generate_answer(question, chunks, confidence)

        # Check if any expected keyword appears in the answer
        answer_lower = answer.lower()
        kw_matched = any(kw.lower() in answer_lower for kw in expected_kws)
        is_fallback = not is_success or answer.strip().startswith("I'm sorry")

        if is_fallback:
            fallback_count += 1
            status = "❌ FALLBACK"
        elif kw_matched:
            correct += 1
            status = "✅ CORRECT"
        else:
            status = "⚠️  PARTIAL"

        print(f"[{i:02d}] {status}")
        print(f"     Q: {question}")
        print(f"     Expected keywords: {expected_kws}")
        print(f"     Confidence: {confidence:.3f}")
        print(f"     Answer snippet: {answer[:120]}...")
        print()

    total = len(cases)
    accuracy = round((correct / total) * 100, 1)
    fallback_rate = round((fallback_count / total) * 100, 1)

    print(f"{'='*60}")
    print(f"  Results:")
    print(f"  Total questions : {total}")
    print(f"  Correct         : {correct}  ({accuracy}%)")
    print(f"  Fallback        : {fallback_count}  ({fallback_rate}%)")
    print(f"  Target accuracy : 80%")
    print(f"  Status          : {'✅ PASSED' if accuracy >= 80 else '❌ BELOW TARGET'}")
    print(f"{'='*60}\n")

    return accuracy


if __name__ == "__main__":
    # Optionally load from CSV
    csv_path = os.path.join(os.path.dirname(__file__), "test_dataset.csv")
    if os.path.exists(csv_path):
        cases = []
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                cases.append({
                    "question": row["question"],
                    "expected_keywords": [k.strip() for k in row.get("expected_keywords", "").split("|")]
                })
        run_eval(cases)
    else:
        run_eval()
