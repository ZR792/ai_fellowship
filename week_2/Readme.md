🧠 AI Chatbot with Multi-Agent System
📌 Overview

This project is part of my AI Fellowship (Week 2 Task) where I built a chat-based application that demonstrates:

Conversational LLMs

Prompt Engineering fundamentals

Multi-Agent system design

A clean Streamlit-based UI

The chatbot supports different roles (agents) that respond in unique ways depending on the system prompt:

👔 Professional Assistant – Formal, business-like responses

🧑‍💻 Technical Expert – Detailed technical explanations

🎨 Creative Companion – Imaginative and artistic responses

Users can interact with any agent, maintain conversation history, and even download their chat sessions for later reference.

⚙️ Features

✅ Command-line chat loop (initial implementation)
✅ Error handling and conversation history
✅ Three system prompts for different response styles
✅ Streamlit web interface with:

💬 Chat-like UI

🔀 Agent selector (choose role dynamically)

📜 Chat history viewer

🗑️ Clear chat option

⬇️ Export chat history (JSON)

🛠️ Tech Stack

Python 3.9+

OpenAI API (Chat Completions)

Streamlit (UI)

Agno (for tools & agents)

dotenv (environment variable management)

📂 Project Structure
│── Chatbot.py      # Agents & tools logic
│── main.py         # Streamlit UI
│── requirements.txt # Dependencies
│── .env            # API keys (not committed to repo)
│── README.md

🚀 Setup Instructions

1️⃣ Clone this repository

git clone https://github.com/your-username/ai-chatbot.git
cd ai-chatbot


2️⃣ Create & activate a virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Add your API key
Create a .env file in the root folder and add:

OPENAI_API_KEY=your_api_key_here


5️⃣ Run the Streamlit app

streamlit run main.py

🎯 Usage

Choose an Agent Role from the sidebar (Professional, Technical, Creative).

Type your question in the chat box and press Enter.

View responses in a chat-style UI.

Clear chat anytime using the button.

Download the full conversation for future use.

📖 Example Prompts

Professional Assistant:

"Can you draft a professional reply to a client asking about project delays?"

Technical Expert:

"Explain Python’s memory management."

Creative Companion:

"Write a short fantasy story about a time-traveling bird."

📝 Reflection

Through this project, I learned how system prompts drastically shape responses from LLMs. The same input can sound formal, technical, or creative depending on prompt engineering. I also practiced building a multi-agent system, integrating APIs, handling errors, and creating a user-friendly Streamlit UI.

⭐ Future Improvements

Add authentication (user login)

Persistent memory across sessions (database)

Support for more roles/agents

Voice input/output integration