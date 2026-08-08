import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="api-key.env")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

story = "The sun rises in the east and sets in the west."
question_count = 3

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

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.3-70b-versatile",
    response_format={"type": "json_object"}
)
print(chat_completion.choices[0].message.content)