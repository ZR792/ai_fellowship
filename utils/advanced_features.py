from transformers import pipeline
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure required NLTK resources are available:
for resource in ['punkt', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)

# Load Hugging Face sentiment analysis pipeline: 
sentiment_pipeline = pipeline("sentiment-analysis")

# Download NLTK tokenizer resources 
nltk.download('punkt', quiet=True)

def analyze_sentiment(text):
    """
    Perform sentiment analysis using a Hugging Face model.
    Returns label (POSITIVE/NEGATIVE/NEUTRAL) and score.
    """
    results = sentiment_pipeline(text)
    # Hugging Face sentiment-analysis returns list of dicts, pick first:
    return results[0]

def text_statistics(text):
    """
    Calculate basic text statistics: readability score, word frequency, etc.
    """
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)

    word_count = len(words)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count else 0

    syllable_count = sum([count_syllables(word) for word in words if word.isalpha()])
    flesch_score = flesch_reading_ease(word_count, sentence_count, syllable_count)

    # Word frequency ignoring punctuation:
    word_freq = Counter([w.lower() for w in words if w.isalpha()])
    top_words = word_freq.most_common(10)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": avg_sentence_length,
        "flesch_reading_ease": flesch_score,
        "top_words": top_words
    }

def count_syllables(word):
    """
    Approximate syllable count for a word.
    """
    vowels = "aeiouy"
    count = 0
    prev_char_was_vowel = False
    for char in word.lower():
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    if word.endswith("e"):
        count = max(1, count - 1)
    return max(count, 1)

def flesch_reading_ease(word_count, sentence_count, syllable_count):
    """
    Compute Flesch Reading Ease score.
    """
    if word_count == 0 or sentence_count == 0:
        return 0
    return 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllable_count / word_count))

# Example usage:
if __name__ == "__main__":
    user_text = input("Enter text for sentiment and statistics: ")

    sentiment_result = analyze_sentiment(user_text)
    stats_result = text_statistics(user_text)

    print("\n--- Sentiment Analysis ---")
    print(f"Label: {sentiment_result['label']}")
    print(f"Score: {sentiment_result['score']:.2f}")

    print("\n--- Text Statistics ---")
    print(f"Word Count: {stats_result['word_count']}")
    print(f"Sentence Count: {stats_result['sentence_count']}")
    print(f"Avg Sentence Length: {stats_result['avg_sentence_length']:.2f} words")
    print(f"Flesch Reading Ease Score: {stats_result['flesch_reading_ease']:.2f}")
    print(f"Top 10 Words: {stats_result['top_words']}")
