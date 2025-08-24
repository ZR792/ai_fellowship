import time
import os
from transformers import pipeline
import google.generativeai as genai
from dotenv import load_dotenv
from config import SUMMARY_MODEL

load_dotenv()

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Hugging Face summarizer (DistilBART):
hf_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Gemini model
GEMINI_MODEL = SUMMARY_MODEL 

# ------------------------------
# Helper Function for error handling and Rate limiting:
# ------------------------------
def safe_gemini_summarize(text, retries=3, delay=2):
    """
    Summarize text using Gemini with error handling and retries
    """
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(f"Summarize this text:\n{text}")
            return response.text
        except Exception as e:
            print(f"Gemini error: {e}, retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
    return "Gemini API failed after retries."

def safe_hf_summarize(text, retries=3, delay=2, max_length=150, min_length=30):
    """
    Summarize text using Hugging Face DistilBART with error handling and retries
    """
    for attempt in range(retries):
        try:
            output = hf_summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return output[0]['summary_text']
        except Exception as e:
            print(f"HuggingFace error: {e}, retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
    return "HuggingFace API failed after retries."

# ------------------------------
# Main function: Compare models:
# ------------------------------
def compare_models(text):
    """
    Returns:
        gemini_summary, hf_summary, gemini_time, hf_time
    """
    # Gemini summarization:
    start_time = time.time()
    gemini_summary = safe_gemini_summarize(text)
    gemini_time = time.time() - start_time

    # Hugging Face summarization:
    start_time = time.time()
    hf_summary = safe_hf_summarize(text)
    hf_time = time.time() - start_time

    return gemini_summary, hf_summary, gemini_time, hf_time
