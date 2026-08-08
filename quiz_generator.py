import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv(dotenv_path="api-key.env")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def normalize_question(question, index):
    labels = ["A", "B", "C", "D"]
    raw_options = question.get("options", [])

    labeled_options = []
    for i, option in enumerate(raw_options):
        if isinstance(option, dict):
            text = option.get("text") or str(option)
        else:
            text = option.strip()
        labeled_options.append(f"{labels[i]}) {text}")

    raw_correct = (
        question.get("correct_answer") or
        question.get("correctAnswer") or
        question.get("correct") or
        question.get("correct_index")
    )

    correct_letter = "A"

    if raw_correct is not None:
        raw_str = str(raw_correct).strip()

        if raw_str.upper() in labels:
            correct_letter = raw_str.upper()

        elif raw_str.isdigit():
            idx = int(raw_str)
            correct_letter = labels[idx] if idx in range(4) else "A"

        else:
            for i, option in enumerate(raw_options):
                if isinstance(option, dict):
                    text = option.get("text") or str(option)
                else:
                    text = option.strip()
                if raw_str.lower() in text.lower():
                    correct_letter = labels[i]
                    break

    return {
        "id": index,
        "question": question.get("question", ""),
        "options": labeled_options,
        "correct_answer": correct_letter
    }


def generate_questions(story, question_count):
    prompt = f"""
You are a quiz generator. Generate exactly {question_count} multiple-choice questions about this story:

{story}

Return ONLY a JSON object in this exact format:
{{
  "questions": [
    {{
      "question": "question text here",
      "options": ["option 1", "option 2", "option 3", "option 4"],
      "correct_index": 0
    }}
  ]
}}

correct_index is the index of the correct answer (0 for first option, 1 for second, 2 for third, 3 for fourth).
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        raw_text = chat_completion.choices[0].message.content
        print("RAW RESPONSE:", raw_text)
        parsed = json.loads(raw_text)
        raw_questions = parsed["questions"]
        return [normalize_question(q, i) for i, q in enumerate(raw_questions, start=1)]
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []