import streamlit as st
import os
from dotenv import load_dotenv

# Import agents from chatbot.py
from chatbot import professional_agent, technical_agent, creative_agent

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Streamlit UI
st.set_page_config(page_title="Multi-Agent Chatbot", layout="wide")

st.title("🤖 Multi-Agent Chatbot")
st.write("Choose your assistant and start chatting!")

# Sidebar for agent selection
agent_choice = st.sidebar.radio(
    "Select Agent:",
    ("Professional Assistant", "Technical Expert", "Creative Companion")
)

# Pick agent
if agent_choice == "Professional Assistant":
    agent = professional_agent
elif agent_choice == "Technical Expert":
    agent = technical_agent
else:
    agent = creative_agent

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for role, msg in st.session_state.messages:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)

# Input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    try:
        # Get agent response
        response = agent.run(user_input)

        # ✅ FIX: Extract only the text content
        response_text = response.content if hasattr(response, "content") else str(response)

        st.session_state.messages.append(("assistant", response_text))
        st.chat_message("assistant").markdown(response_text)

    except Exception as e:
        st.session_state.messages.append(("assistant", f"⚠️ Error: {str(e)}"))
        st.chat_message("assistant").markdown(f"⚠️ Error: {str(e)}")

# Sidebar tools
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Option to download chat history
if st.sidebar.button("📥 Download Chat History"):
    chat_text = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.messages])
    st.sidebar.download_button(
        "Download Chat",
        chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

