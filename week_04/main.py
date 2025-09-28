import streamlit as st
from summarizer import summarize_article, answer_question

st.set_page_config(page_title="AI News Summarizer", layout="wide")

st.title("📰 AI News Summarizer & Q&A ")

# Sidebar info
st.sidebar.header("ℹ️ About")
st.sidebar.write(
    "This app summarizes long news articles using **Google Gemini API** "
    "and allows you to ask follow-up questions."
)

# Text input for article
st.subheader("📄 Paste your article text below:")
article_text = st.text_area("Enter article text:", height=250)

if article_text.strip():
    # Show stats
    words = len(article_text.split())
    chars = len(article_text)
    st.write(f"**📏 Original article length:** {words} words, {chars} characters")

    # Summarization section
    st.subheader("📝 Summaries")
    temp_options = [0.1, 0.7, 1.0]
    for t in temp_options:
        with st.expander(f"Summary (temperature={t})"):
            summary = summarize_article(article_text, temperature=t)
            st.write(summary)

    # Q&A section
    st.subheader("❓ Ask questions about the article")
    question = st.text_input("Type your question here:")

    if st.button("Get Answer"):
        if question.strip():
            answer = answer_question(article_text, question)
            st.success(answer)
        else:
            st.warning("Please enter a question.")

else:
    st.info("👆 Paste an article above to start.")
