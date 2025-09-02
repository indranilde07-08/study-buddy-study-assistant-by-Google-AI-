import google.generativeai as genai

genai.configure(api_key="AIzaSyD_Hw6mev6WeYGUId9VtIg4uOadIcYw__8")  

def generate_summary(text,lines=250):
    prompt = f"Summarize the following text in {lines}lines:\n\n{text}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text

