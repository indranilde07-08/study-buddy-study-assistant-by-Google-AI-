import json
import google.generativeai as genai
def generate_quiz(text, num_questions=5):
    prompt = f"""
    Create {num_questions} multiple-choice questions from this text.
    Return only JSON like this:
    [
      {{
        "question": "What is ...?",
        "options": ["A) ...","B) ...","C) ...","D) ..."],
        "answer": "B",
        "explanation": "Why B is correct..."
      }}
    ]
    Text:
    {text}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    raw = response.candidates[0].content.parts[0].text.strip()

    # remove markdown formatting if any
    raw = raw.strip("```json").strip("```")

    try:
        quiz = json.loads(raw)
    except Exception as e:
        print("JSON parse error:", e, raw)  # debugging
        quiz = []
    return quiz

