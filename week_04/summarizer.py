import os
import textwrap
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print(" Please add GEMINI_API_KEY to your .env file.")
    exit(1)

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL = "gemini-1.5-flash"   

def call_gemini(prompt, temperature=0.7, max_output_tokens=400):
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens
        }
    )
    return response.text.strip()

def summarize_article(article_text, temperature=0.7):
    prompt = f"""
    Summarize the following news article in 3–4 sentences.
    Article:
    {article_text}
    """
    return call_gemini(prompt, temperature=temperature)

def answer_question(article_text, question):
    prompt = f"""
    Based on the article below, answer the following question.
    If the answer is not in the article, reply: "Not stated in the article."

    Question: {question}
    Article: {article_text}
    """
    return call_gemini(prompt, temperature=0.2)

def main():
    print("🚀 AI News Summarizer & Q&A Tool (Gemini Edition)")
    print("Paste your article text (end with an empty line):")

    # Multiline input
    lines = []
    while True:
        line = input()
        if line.strip() == "" and len(lines) > 0:
            break
        lines.append(line)
    article_text = "\n".join(lines)

    words = len(article_text.split())
    chars = len(article_text)
    print(f"\n📏 Original article length: {words} words, {chars} characters.\n")

    # Part 1: Summaries at different temperatures
    for t in [0.1, 0.7, 1.0]:
        print(f"\n📝 Summary (temperature={t}):")
        summary = summarize_article(article_text, temperature=t)
        print(textwrap.fill(summary, width=80))
        print("-" * 60)

    # Part 2: Interactive Q&A
    print("\n❓ Now ask questions about the article (type 'quit' after 3 questions to exit).")
    q_count = 0
    while True:
        q = input(f"Question {q_count+1}: ")
        if q.lower() in ["quit", "exit"] and q_count >= 3:
            break
        answer = answer_question(article_text, q)
        print("Answer:", answer, "\n")
        q_count += 1

if __name__ == "__main__":
    main()
