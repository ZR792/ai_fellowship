# 🧠 AI Chatbot with Multi-Agent System

## 📌 Overview

This project is part of my **AI Fellowship (Week 2 Task)** where I built a chat-based application that demonstrates:

- Conversational LLMs
- Prompt Engineering fundamentals
- Multi-Agent system design
- A clean Streamlit-based UI

The chatbot supports different roles (agents) that respond in unique ways depending on the system prompt:

- 👔 **Professional Assistant** – Formal, business-like responses  
- 🧑‍💻 **Technical Expert** – Detailed technical explanations  
- 🎨 **Creative Companion** – Imaginative and artistic responses  

Users can interact with any agent, maintain conversation history, and even download their chat sessions for later reference.

---

## ⚙️ Features

- ✅ Command-line chat loop (initial implementation)  
- ✅ Error handling and conversation history  
- ✅ Three system prompts for different response styles  
- ✅ Streamlit web interface with:  
  - 💬 Chat-like UI  
  - 🔀 Agent selector (choose role dynamically)  
  - 📜 Chat history viewer  
  - 🗑️ Clear chat option  
  - ⬇️ Export chat history (JSON)

---

## 🛠️ Tech Stack

- Python 3.9+  
- OpenAI API (Chat Completions)  
- Streamlit (UI)  
- Agno (for tools & agents)  
- dotenv (environment variable management)

---



## 📂 Project Structure
week_2/
│── Chatbot.py          # Agents & tools logic
│── main.py             # Streamlit UI
│── requirements.txt    # Dependencies
│── .env                # API keys (not committed to repo)
│── README.md
│
├── data/
│   └── sample_text
│
└── tools/
    ├── __pycache__/
    │    ├── __init__.cpython-313.pyc
    │    ├── quotes.cpython-313.pyc
    │    └── tool_base.cpython-313.pyc
    ├── quotes.py
    └── tool_base.py


---

## 🚀 Setup Instructions

1️⃣ **Clone this repository**

```bash
git clone https://github.com/ZR792/ai_fellowship.git
cd week_2
```
2️⃣ **Create & activate a virtual environment**
# Windows
task_2\Scripts\activate

3️⃣ **Install dependencies**
pip install -r requirements.txt

4️⃣ **Add your API key**
Create a .env file in the root folder and add:

5️⃣ **Run the Streamlit app**
streamlit run main.py

### 🎯 Usage

- Choose an Agent Role from the sidebar (Professional, Technical, Creative).
- Type your question in the chat box and press Enter.
- View responses in a chat-style UI.
- Clear chat anytime using the button.
- Download the full conversation for future use.

### 📝 Reflection

Through this project, I learned how system prompts drastically shape responses from LLMs. The same input can sound formal, technical, or creative depending on prompt engineering. I also practiced:

* Building a multi-agent system
* Integrating APIs
* Handling errors
* Creating a user-friendly Streamlit UI

### ⭐ Future Improvements

* Add authentication (user login)
* Persistent memory across sessions (database)
* Support for more roles/agents
* Voice input/output integration
