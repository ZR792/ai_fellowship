from pathlib import Path
import textwrap
from gemini_utils import image_caption, document_ocr, chart_analysis, embed_texts, generate_text

BASE = Path(__file__).resolve().parent
IMAGES_DIR = BASE / "images"
OUTPUT_DIR = BASE / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
EXAMPLE_MD = OUTPUT_DIR / "example_outputs.md"

PHOTO = IMAGES_DIR / "photo.jpg"
DOCUMENT = IMAGES_DIR / "document.png"
CHART = IMAGES_DIR / "chart.png"
LONG_TEXT = BASE / "long_text.pdf"

def write_md(lines):
    EXAMPLE_MD.write_text("\n".join(lines), encoding="utf8")
    print("[*] Wrote output to", EXAMPLE_MD)

def debug_paths():
    print("[DEBUG] BASE folder:", BASE)
    print("[DEBUG] IMAGES_DIR:", IMAGES_DIR)
    print("[DEBUG] OUTPUT_DIR:", OUTPUT_DIR)
    print("[DEBUG] PHOTO exists?:", PHOTO.exists(), PHOTO)
    print("[DEBUG] DOCUMENT exists?:", DOCUMENT.exists(), DOCUMENT)
    print("[DEBUG] CHART exists?:", CHART.exists(), CHART)
    print("[DEBUG] LONG_TEXT exists?:", LONG_TEXT.exists(), LONG_TEXT)

def run_photo():
    out = []
    out.append("## Photo Analysis\n")
    if PHOTO.exists():
        out.append("**Image file:** photo.jpg\n")
        cap = image_caption(str(PHOTO))
        out.append("**Caption / Description:**\n")
        out.append(textwrap.fill(cap, width=100) + "\n")
    else:
        out.append(f"photo.jpg not found at {PHOTO} - skipping.\n")
    return out

def run_document():
    out = []
    out.append("## Document OCR\n")
    if DOCUMENT.exists():
        out.append("**Image file:** document.png\n")
        txt = document_ocr(str(DOCUMENT))
        out.append("**OCR text (first 800 chars):**\n")
        out.append("```\n" + (txt[:800] if txt else "(no text extracted)") + "\n```\n")
    else:
        out.append(f"document.png not found at {DOCUMENT} - skipping.\n")
    return out

def run_chart():
    out = []
    out.append("## Chart Analysis\n")
    if CHART.exists():
        out.append("**Image file:** chart.png\n")
        analysis = chart_analysis(str(CHART))
        out.append("**Chart analysis (vision/model):**\n")
        out.append(analysis + "\n")
    else:
        out.append(f"chart.png not found at {CHART} - skipping.\n")
    return out

# ---------------------- Long-context (PDF support + small local RAG demo) ----------------------
import textwrap

# Path to the long document (can be .txt or .pdf)
LONG_TEXT_TXT = BASE / "long_text.txt"
LONG_TEXT_PDF = BASE / "long_text.pdf"

def extract_text_from_pdf(pdf_path):
    """
    Try pdfplumber first (better); if not available fall back to PyPDF2.
    Returns a single string with all page text concatenated.
    """
    pdf_path = Path(pdf_path)
    text = ""
    # try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            for p in pdf.pages:
                page_text = p.extract_text() or ""
                text += "\n\n" + page_text
        print("[long-context] Extracted text using pdfplumber.")
        return text.strip()
    except Exception:
        # fall back to PyPDF2
        try:
            from PyPDF2 import PdfReader
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += "\n\n" + (page.extract_text() or "")
            print("[long-context] Extracted text using PyPDF2 fallback.")
            return text.strip()
        except Exception as e:
            print("[long-context] PDF text extraction failed:", e)
            return ""

def save_text_for_reuse(txt, out_path=LONG_TEXT_TXT):
    try:
        out_path.write_text(txt, encoding="utf8")
        print(f"[long-context] Saved extracted text to {out_path}")
    except Exception as e:
        print("[long-context] Failed to save extracted text:", e)

def run_long_context():
    lines = []
    lines.append("## Long-context RAG demo\n")
    # If there's already a plain text file, use it (fast)
    if LONG_TEXT_TXT.exists():
        txt = LONG_TEXT_TXT.read_text(encoding="utf8", errors="ignore")
        lines.append(f"Loaded existing long_text.txt ({len(txt)} chars)\n")
        lines.append("Preview:\n")
        lines.append("```\n" + txt[:800] + "\n```\n")
    elif LONG_TEXT_PDF.exists():
        print("[long-context] Found PDF, extracting text now...")
        txt = extract_text_from_pdf(LONG_TEXT_PDF)
        if not txt:
            lines.append("Failed to extract text from PDF.\n")
        else:
            lines.append(f"Extracted {len(txt)} characters from long_text.pdf\n")
            lines.append("Preview:\n")
            lines.append("```\n" + txt[:800] + "\n```\n")
            # save for reuse
            try:
                save_text_for_reuse(txt)
            except Exception:
                pass
    else:
        lines.append("No long_text.txt or long_text.pdf found - skipping long-context demo.\n")
        return lines

    # --- Optional: tiny local RAG demo (only if dependencies installed) ---
    try:
        # chunk a little
        chunk_chars = 3000
        overlap = 300
        chunks = []
        i = 0
        while i < len(txt):
            chunks.append(txt[i:i+chunk_chars])
            i = max(0, i + chunk_chars - overlap)
        lines.append(f"Chunks created: {len(chunks)}\n")

        # compute embeddings locally (sentence-transformers) and build FAISS index
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            import faiss
            embed_model = SentenceTransformer("all-MiniLM-L6-v2")
            emb = embed_model.encode(chunks, convert_to_numpy=True, show_progress_bar=False).astype("float32")
            # normalize + build index
            faiss.normalize_L2(emb)
            d = emb.shape[1]
            index = faiss.IndexFlatIP(d)
            index.add(emb)
            lines.append("FAISS index built (local embeddings).\n")

            # Example query to show retrieval
            sample_q = "Summarize the main contributions in two sentences."
            qv = embed_model.encode([sample_q], convert_to_numpy=True).astype("float32")
            faiss.normalize_L2(qv)
            D, I = index.search(qv, 4)
            hits = [chunks[int(idx)][:400].replace("\n"," ") for idx in I[0] if idx >= 0]
            lines.append("Sample retrieval previews (top hits):\n")
            for h in hits:
                lines.append("- " + h + "\n")
            # build a strict RAG prompt and call the (local or Gemini) generator
            context = "\n\n---\n".join([h for h in hits])
            prompt = (
                "You are an assistant. Use ONLY the context below to answer the question. "
                "If the answer is not in the context, say 'Not enough information in the provided context.'\n\n"
                f"Context:\n{context}\n\nQuestion: {sample_q}\n\nAnswer concisely and cite chunk indices."
            )
            rag_ans = generate_text(prompt)
            lines.append("RAG answer (sample):\n")
            lines.append(rag_ans + "\n")
        except Exception as e:
            lines.append("[long-context] Local RAG demo skipped (missing sentence-transformers/faiss) or failed: " + str(e) + "\n")
    except Exception as e:
        lines.append("[long-context] Error in RAG demo: " + str(e) + "\n")

    return lines

# end of long-context section


def main():
    debug_paths()
    lines = []
    lines += run_photo()
    lines += ["\n"]
    lines += run_document()
    lines += ["\n"]
    lines += run_chart()
    lines += ["\n"]
    lines += run_long_context()
    write_md(lines)
    print("Done.")

if __name__ == "__main__":
    main()

# preproc_ocr.py (paste into your multimodal file or gemini_utils)
from PIL import Image, ImageOps, ImageFilter
import pytesseract
import numpy as np

def ocr_with_preprocessing(path: str, scale=2, denoise=True, use_threshold=True):
    img = Image.open(path).convert("RGB")
    # Convert to grayscale
    gray = ImageOps.grayscale(img)
    # Resize to help OCR (scale factor)
    new_size = (int(gray.width * scale), int(gray.height * scale))
    gray = gray.resize(new_size, resample=Image.BILINEAR)
    # Optional denoising / sharpening
    if denoise:
        gray = gray.filter(ImageFilter.MedianFilter(size=3))
        gray = gray.filter(ImageFilter.SHARPEN)
    # Optional adaptive threshold to increase contrast
    if use_threshold:
        arr = np.array(gray)
        # simple global threshold (Otsu would be better if OpenCV available)
        # Use PIL point for speed:
        thresh = 128
        gray = gray.point(lambda p: 255 if p > thresh else 0)
    # Save debug preprocessed image if you want
    # gray.save("debug_preproc.png")
    text = pytesseract.image_to_string(gray, lang="eng", config="--psm 3")
    return text
