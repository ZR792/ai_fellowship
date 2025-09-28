from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from tools.quotes import MotivationTool
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# --- Define Specialized Agents (your custom tools) ---
web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[DuckDuckGoTools()],
    instructions="Always include the sources",
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True,
                         stock_fundamentals=True, company_info=True)],
    instructions="Use tables to display data",
    show_tool_calls=True,
    markdown=True,
)

motivation_agent = Agent(
    name="Motivation Agent",
    role="Encourage the user",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[MotivationTool()],
    instructions="Use motivational quotes when user feels low",
    show_tool_calls=True,
    markdown=True,
)

# --- Create Team Agent ---
agent_team = Agent(
    team=[web_agent, finance_agent, motivation_agent],
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    markdown=True,
)

# --- System Prompt Selector ---
system_prompts = {
    "professional": "You are a professional assistant. Respond in a formal, business-like way.",
    "creative": "You are a creative companion. Respond imaginatively, with artistic flair.",
    "technical": "You are a technical expert. Explain with depth, precision, and clarity."
}

def chat():
    print("Chatbot with Custom Tools (type 'exit' to quit)")
    print("Choose prompt style: professional / creative / technical")
    style = input("Style: ").strip().lower()
    system_prompt = system_prompts.get(style, system_prompts["professional"])

    history = [{"role": "system", "content": system_prompt}]

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        history.append({"role": "user", "content": query})
        try:
            response = agent_team.get_response(query, conversation=history)
            print("Bot:", response.content)
            history.append({"role": "assistant", "content": response.content})
        except Exception as e:
            print("Error:", str(e))

# --- Individual Agents for Streamlit UI ---
professional_agent = Agent(
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    instructions=system_prompts["professional"],
    markdown=True,
)

technical_agent = Agent(
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    instructions=system_prompts["technical"],
    markdown=True,
)

creative_agent = Agent(
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    instructions=system_prompts["creative"],
    markdown=True,
)

if __name__ == "__main__":
    chat()
