import json
import re
from config import client


class AIGenerator:

    @staticmethod
    def generate_questions(content, num=5):
        prompt = f"""
Generate {num} multiple choice questions on: {content}.

STRICT RULES:
- Output ONLY valid JSON
- No markdown outside JSON
- Start with [ and end with ]
- Each option must start with A., B., C., D.
- If the question involves code, INCLUDE the full code inside the question
- Code must be inside triple quotes like '''code'''

Format:
[
  {{
    "question": "Question text. If code is needed, include it like this: ''' code here '''",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "A",
    "explanation": "..."
  }}
]
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return AIGenerator.parse_questions(response.text)

        except Exception as exceptions:
            print("⚠️ API Error:", exceptions)
            return AIGenerator.fallback()

    @staticmethod
    def parse_questions(raw_text):
        try:
            match = re.search(r"\[.*\]", raw_text, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")

            return json.loads(match.group(0))

        except Exception as expections:
            print("❌ Parsing Error:", expections)
            print("RAW:", raw_text)
            return []

    @staticmethod
    def fallback():
        return [
            {
                "question": "What is OOP?",
                "options": ["A. Concept", "B. Language", "C. Tool", "D. None"],
                "answer": "A",
                "explanation": "OOP is a programming concept."
            }
        ]