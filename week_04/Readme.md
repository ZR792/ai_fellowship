# AI News Summarizer & Q&A Tool 🚀  

## 📌 Overview  
This project is part of **Week 4 of the AI Fellowship**. The goal was to build a Python tool that uses the **Gemini API** to:  
- Summarize any news article into **3–4 sentences**.  
- Allow interactive **Q&A about the article**.  
- Experiment with **temperature settings** to see how output changes.  

I later extended the project with a simple **Streamlit frontend** for better usability.  

---

## 🛠️ Tech Stack  
- **Language**: Python 3.10+  
- **Framework**: Streamlit (for frontend UI)  
- **LLM API**: Google Gemini 1.5 Flash  
- **Libraries**:  
  - `google-generativeai` (Gemini API client)  
  - `python-dotenv` (for environment variables)  
  - `textwrap` (formatting output)  

---

## 📂 Project Structure  
````
Week_04_AI_Fellowship/
│── summarizer.py # CLI-based summarizer & QnA
│── main.py # Streamlit frontend app
│── observations.md # Notes on temperature tuning
│── README.md # Project documentation

````

---

## ⚡ Features  
- Summarize any news article text in **3–4 sentences**.  
- Generate **summaries at 3 different temperatures**: 0.1 (robotic), 0.7 (balanced), 1.0 (creative).  
- Ask **interactive questions** about the article (Q&A).  
- Compare and record **parameter tuning results** in `observations.md`.  
- Streamlit UI for **easy testing and demo**.  

---

## 📖 What I Did & Learnt  

### ✅ What I Did  
- Built a Python script (`summarizer.py`) to call the **Gemini API**.  
- Implemented a **summarization engine**.  
- Added an **interactive Q&A system**.  
- Tested different **temperature values** and documented results.  
- Created a **Streamlit app (main.py)** for a simple frontend.  

### 🎓 What I Learnt  
- How to use **LLM APIs** (Gemini).  
- How **temperature parameter** affects creativity vs accuracy.  
- How to design **prompts** for summarization and Q&A.  
- Basics of turning a script into a **CLI tool** and then into a **Streamlit frontend**.  
- Importance of **environment variables (.env)** for API security.  

---

## ▶️ How to Run the Project  

### 1. Clone Repository  
```bash
git clone <your-repo-url>
cd Week_04_AI_Fellowship

pip install -r requirements.txt

streamlit run main.py
```
---

### 🚀 Future Improvements

- Support for article URLs (auto web scraping).
- Fun custom summary styles (pirate, comedian, sports commentator).
- Deploy Streamlit app online (Streamlit Cloud / Hugging Face Spaces).