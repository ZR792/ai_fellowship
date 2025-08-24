from transformers import AutoTokenizer

# Load a default tokenizer (BERT base):
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def analyze_tokenization(text: str):
    """
    Perform tokenization analysis using Hugging Face tokenizer.
    Returns a dictionary with token details.
    """
    if not text.strip():
        return {
            "tokens": [],
            "token_count": 0,
            "token_ids": [],
            "attention_mask": [],
            "error": "Text cannot be empty for tokenization."
        }

    # Tokenize and get detailed info:
    encoded = tokenizer(text, return_tensors="pt")
    tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"][0])

    return {
        "tokens": tokens,
        "token_count": len(tokens),            
        "token_ids": encoded["input_ids"][0].tolist(),
        "attention_mask": encoded["attention_mask"][0].tolist()
    }
