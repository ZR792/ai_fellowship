import streamlit as st
from utils.llm_helpers import compare_models  
from utils.tokenizer_helpers import analyze_tokenization  
from utils.advanced_features import analyze_sentiment, text_statistics  

st.set_page_config(page_title="Text Analysis Tool", page_icon="📝", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📝 Text Analysis Tool</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Analyze your text with model comparison, tokenization, sentiment, and readability statistics.</p>", unsafe_allow_html=True)

user_text = st.text_area("**Enter your text below:**", height=200, placeholder="Type or paste your text here...")

if st.button("🚀 Analyze"):
    if not user_text.strip():
        st.warning("⚠️ Please enter some text before analyzing.")
    else:
        # --- Summarization (Gemini & DistilBART) with timing and retries:
        with st.spinner("⏳ Generating summaries..."):
            gemini_summary, hf_summary, gemini_time, hf_time = compare_models(user_text)

        # --- Tokenization Analysis:
        with st.spinner("⏳ Analyzing tokenization..."):
            token_stats = analyze_tokenization(user_text)

        # --- Sentiment Analysis:
        with st.spinner("⏳ Analyzing sentiment..."):
            sentiment_result = analyze_sentiment(user_text)

        # --- Text Statistics:
        with st.spinner("⏳ Calculating text statistics..."):
            stats_result = text_statistics(user_text)

        st.markdown("---")
        st.markdown("### 🔹 **Gemini Summary**")
        st.success(gemini_summary)
        if gemini_time:
            st.info(f"Time taken: {gemini_time:.2f} seconds")

        st.markdown("### 🔹 **DistilBART Summary**")
        st.success(hf_summary)
        if hf_time:
            st.info(f"Time taken: {hf_time:.2f} seconds")

        st.markdown("### 🔹 **Tokenization Analysis**")
        st.write(f"**Token Count:** {token_stats.get('token_count', 0)}")
        st.markdown("**Tokens Preview (first 20):**")
        st.code(", ".join(token_stats.get('tokens', [])[:20]))

        st.markdown("### 🔹 **Sentiment Analysis**")
        st.info(f"**Label:** {sentiment_result['label']} | **Confidence Score:** {sentiment_result['score']:.2f}")

        st.markdown("### 🔹 **Text Statistics**")
        st.write(f"**Word Count:** {stats_result['word_count']}")
        st.write(f"**Sentence Count:** {stats_result['sentence_count']}")
        st.write(f"**Average Sentence Length:** {stats_result['avg_sentence_length']:.2f} words")
        st.write(f"**Flesch Reading Ease:** {stats_result['flesch_reading_ease']:.2f}")
        st.markdown("**Top 10 Words:**")
        st.markdown(
            "<div style='display: flex; flex-wrap: wrap; gap: 10px;'>"
            + "".join([f"<span style='background:#f0f0f0; padding:5px 10px; border-radius:5px;'>{word}: {count}</span>" for word, count in stats_result['top_words']])
            + "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✅ **Analysis Complete!**")
