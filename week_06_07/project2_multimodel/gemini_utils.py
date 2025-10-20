import os, time, traceback
from typing import List, Dict, Any

# Try to import Gemini SDK
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

USE_GEMINI = bool(GEMINI_KEY)

# Lazy imports for gemini and local models
client = None

if USE_GEMINI:
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_KEY)
    except Exception as e:
        print("[gemini_utils] Failed to initialize google-genai client:", e)
        USE_GEMINI = False

# Local fallbacks
_local_blip = None
_local_blip_processor = None
_local_embed_model = None
_local_gen_tokenizer = None
_local_gen_model = None

def init_local_models():
    global _local_blip, _local_blip_processor, _local_embed_model, _local_gen_tokenizer, _local_gen_model
    if _local_blip is None:
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer, AutoModelForSeq2SeqLM
            _local_blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            _local_blip = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        except Exception as e:
            print("[gemini_utils] BLIP local load failed:", e)
            _local_blip = _local_blip_processor = None
    if _local_embed_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _local_embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print("[gemini_utils] local embed model load failed:", e)
            _local_embed_model = None
    if _local_gen_model is None:
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            _local_gen_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
            _local_gen_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        except Exception as e:
            print("[gemini_utils] local generator load failed:", e)
            _local_gen_tokenizer = _local_gen_model = None

# ---------------- Gemini wrappers ----------------
def _gemini_image_caption(path: str) -> str:
    """
    Use Gemini Vision (if available) to caption an image.
    """
    global client
    try:
        with open(path, "rb") as f:
            data = f.read()
        # Use the models.generate_content with images attachment if supported.
        # The google-genai SDK supports sending binary image as part of 'inputs' in some releases.
        # Here we pass a text prompt and the SDK will attach the image bytes.
        prompt = (
            "You are an assistant that describes images for accessibility. "
            "Return: 1) a 1-sentence caption. 2) three short observations (bullet list). 3) accessibility notes."
        )
        resp = client.models.generate_content(
            model="gemini-vision-preview",
            # many SDK versions accept `content` or `inputs` — prefer `contents` with image bytes in the latest
            # If your SDK version differs, you may need to consult local SDK docs.
            contents=[{"type":"image", "image_bytes": data, "caption": prompt}]
        )
        # Try common response shapes
        text = getattr(resp, "text", None)
        if not text and hasattr(resp, "candidates") and len(resp.candidates):
            text = resp.candidates[0].content
        return text or str(resp)
    except Exception as e:
        print("[gemini_utils] Gemini image caption error:", e)
        traceback.print_exc()
        raise

def _gemini_document_ocr(path: str) -> str:
    """
    Use Gemini Vision OCR to extract text.
    """
    global client
    try:
        with open(path, "rb") as f:
            data = f.read()
        prompt = "Extract all readable text from the image. Return plain text only."
        resp = client.models.generate_content(
            model="gemini-vision-preview",
            contents=[{"type":"image", "image_bytes": data, "caption": prompt}]
        )
        text = getattr(resp, "text", None)
        if not text and hasattr(resp, "candidates") and len(resp.candidates):
            text = resp.candidates[0].content
        return text or ""
    except Exception as e:
        print("[gemini_utils] Gemini document OCR error:", e)
        traceback.print_exc()
        raise

def _gemini_chart_analysis(path: str) -> str:
    """
    Ask Gemini Vision to analyze the chart and return structured text.
    """
    global client
    try:
        with open(path, "rb") as f:
            data = f.read()
        prompt = (
            "You are a chart understanding assistant. Detect the chart type (bar/line/etc), "
            "extract axis labels, legend entries, and summarize main trends in 2-3 sentences."
        )
        resp = client.models.generate_content(
            model="gemini-vision-preview",
            contents=[{"type":"image", "image_bytes": data, "caption": prompt}]
        )
        text = getattr(resp, "text", None)
        if not text and hasattr(resp, "candidates") and len(resp.candidates):
            text = resp.candidates[0].content
        return text or ""
    except Exception as e:
        print("[gemini_utils] Gemini chart analysis error:", e)
        traceback.print_exc()
        raise

def _gemini_embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Use Gemini text embedding model to embed a list of strings.
    """
    global client
    try:
        resp = client.models.embed_content(model="gemini-embedding-001", contents=texts)
        embs = []
        for e in resp.embeddings:
            # e might be dict or list
            if isinstance(e, dict):
                v = e.get("embedding") or e.get("values") or list(e.values())[0]
            else:
                v = e
            embs.append(v)
        return embs
    except Exception as e:
        print("[gemini_utils] Gemini embedding error:", e)
        traceback.print_exc()
        raise

def _gemini_generate_text(prompt: str) -> str:
    """
    Use Gemini to generate text from a prompt.
    """
    global client
    try:
        resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = getattr(resp, "text", None)
        if not text and hasattr(resp, "candidates") and len(resp.candidates):
            text = resp.candidates[0].content
        return text or str(resp)
    except Exception as e:
        print("[gemini_utils] Gemini generation error:", e)
        traceback.print_exc()
        raise

# ---------------- Local fallbacks ----------------
def _local_image_caption(path: str) -> str:
    init_local_models()
    global _local_blip_processor, _local_blip
    if _local_blip is None:
        return "Local BLIP model not available."
    try:
        from PIL import Image
        img = Image.open(path).convert("RGB")
        inputs = _local_blip_processor(images=img, return_tensors="pt")
        out = _local_blip.generate(**inputs)
        caption = _local_blip_processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        print("[gemini_utils] local BLIP caption error:", e)
        traceback.print_exc()
        return "Local caption error."

def _local_document_ocr(path: str) -> str:
    # Use pytesseract as fallback
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(path).convert("RGB")
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print("[gemini_utils] local OCR error:", e)
        traceback.print_exc()
        return ""

def _local_chart_analysis(path: str) -> str:
    # simple approach: OCR + short local generation to summarize
    try:
        text = _local_document_ocr(path)
        prompt = (
            "Detected OCR text from the chart:\n\n"
            f"{text[:2000]}\n\n"
            "Based on the OCR, give a short summary of likely chart type and trends (2-3 sentences)."
        )
        return _local_generate_text(prompt)
    except Exception as e:
        print("[gemini_utils] local chart analysis error:", e)
        traceback.print_exc()
        return "Local chart analysis error."

def _local_embed_texts(texts: List[str]) -> List[List[float]]:
    init_local_models()
    global _local_embed_model
    if _local_embed_model is None:
        raise RuntimeError("Local embedding model not available.")
    return _local_embed_model.encode(texts, convert_to_numpy=False).tolist()

def _local_generate_text(prompt: str) -> str:
    init_local_models()
    global _local_gen_model, _local_gen_tokenizer
    if _local_gen_model is None or _local_gen_tokenizer is None:
        return "Local generator not available."
    try:
        inputs = _local_gen_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        out = _local_gen_model.generate(**inputs, max_new_tokens=200)
        text = _local_gen_tokenizer.decode(out[0], skip_special_tokens=True)
        return text
    except Exception as e:
        print("[gemini_utils] local generate error:", e)
        traceback.print_exc()
        return "Local generation error."

# ---------------- Public API ----------------
def image_caption(path: str) -> str:
    if USE_GEMINI:
        try:
            return _gemini_image_caption(path)
        except Exception:
            print("[gemini_utils] Falling back to local BLIP for caption.")
    return _local_image_caption(path)

def document_ocr(path: str) -> str:
    if USE_GEMINI:
        try:
            return _gemini_document_ocr(path)
        except Exception:
            print("[gemini_utils] Falling back to local OCR.")
    return _local_document_ocr(path)

def chart_analysis(path: str) -> str:
    if USE_GEMINI:
        try:
            return _gemini_chart_analysis(path)
        except Exception:
            print("[gemini_utils] Falling back to local chart analysis.")
    return _local_chart_analysis(path)

def embed_texts(texts: List[str]) -> List[List[float]]:
    if USE_GEMINI:
        try:
            return _gemini_embed_texts(texts)
        except Exception:
            print("[gemini_utils] Falling back to local embeddings.")
    return _local_embed_texts(texts)

def generate_text(prompt: str) -> str:
    if USE_GEMINI:
        try:
            return _gemini_generate_text(prompt)
        except Exception:
            print("[gemini_utils] Falling back to local generator.")
    return _local_generate_text(prompt)
