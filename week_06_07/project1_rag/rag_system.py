import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import pdfplumber

# faiss
import faiss

# sentence-transformers for embeddings
from sentence_transformers import SentenceTransformer

# transformers for local generation
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ---------------- Config ----------------
PROJECT_DIR = Path(".") / "project1-rag"
PROJECT_DIR.mkdir(parents=True, exist_ok=True)

PDF_PATH = PROJECT_DIR / "sample.pdf"
CHUNKS_JSON = PROJECT_DIR / "chunks.json"
CHUNKS_SPLIT_JSON = PROJECT_DIR / "chunks_split.json"
EMBEDDINGS_NPY = PROJECT_DIR / "embeddings.npy"
FAISS_INDEX_PATH = PROJECT_DIR / "faiss.index"
RESPONSES_JSON = PROJECT_DIR / "responses.json"
COMPARISON_MD = PROJECT_DIR / "comparison_analysis.md"

# Embedding model (local)
LOCAL_EMBED_MODEL = "all-MiniLM-L6-v2"

# Local generator model (smaller / CPU-friendly)
LOCAL_GEN_MODEL = "google/flan-t5-small"
LOCAL_GEN_MAX_NEW_TOKENS = 200

# Chunking defaults
SMALL_CHUNK_SIZE = 3000
SMALL_CHUNK_OVERLAP = 300
LARGE_CHUNK_SIZE = 9000
LARGE_CHUNK_OVERLAP = 500

# Retrieval default
TOP_K = 4

# ---------------- Helpers ----------------
def extract_text_pdfplumber(pdf_path: str) -> Dict[str, Any]:
    """Extract text from PDF using pdfplumber; returns dict with full_text & page_index."""
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    text = ""
    page_index = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            start_char = len(text)
            text += f"\n\n[PAGE {i+1}]\n" + page_text
            page_index.append({"page": i + 1, "start_char": start_char, "length": len(page_text)})
    return {"full_text": text, "page_index": page_index}

def chunk_text_chars(text: str, chunk_size:int=SMALL_CHUNK_SIZE, overlap:int=SMALL_CHUNK_OVERLAP) -> List[str]:
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunks.append(text[start:end])
        start = max(end - overlap, end)
    return chunks

# ---------------- Embedding (local) ----------------
print("[*] Loading embedding model:", LOCAL_EMBED_MODEL)
embed_model = SentenceTransformer(LOCAL_EMBED_MODEL)

def compute_local_embeddings(text_list: List[str], batch_size: int = 32) -> np.ndarray:
    """Return numpy array float32 of embeddings."""
    emb = embed_model.encode(text_list, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True)
    return np.array(emb, dtype=np.float32)

# ---------------- Local generator (TF/PyTorch) ----------------
print("[*] Preparing local generator:", LOCAL_GEN_MODEL)
tokenizer = AutoTokenizer.from_pretrained(LOCAL_GEN_MODEL)
gen_model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_GEN_MODEL)

def generate_local(prompt: str, max_new_tokens:int=LOCAL_GEN_MAX_NEW_TOKENS) -> str:
    """Generate text locally with the seq2seq model. Works on CPU (may be slower)."""
    # Tokenize & generate
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    out = gen_model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    return text

# ---------------- FAISS functions ----------------
def build_faiss_index(emb_matrix: np.ndarray) -> faiss.Index:
    emb = emb_matrix.copy()
    faiss.normalize_L2(emb)
    d = emb.shape[1]
    idx = faiss.IndexFlatIP(d)
    idx.add(emb)
    return idx

def save_faiss_index(index: faiss.Index, path: Path):
    faiss.write_index(index, str(path))

def load_faiss_index(path: Path) -> faiss.Index:
    return faiss.read_index(str(path))

# ---------------- Main pipeline ----------------
def main_run():
    # 1) Extract PDF text
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Put your PDF at: {PDF_PATH.resolve()} and re-run.")
    print("[*] Extracting PDF:", PDF_PATH)
    extracted = extract_text_pdfplumber(str(PDF_PATH))
    full_text = extracted["full_text"]
    print(f"[+] Extracted {len(full_text)} characters across {len(extracted['page_index'])} pages")

    # Save raw extraction
    with open(CHUNKS_JSON, "w", encoding="utf8") as f:
        json.dump(extracted, f, ensure_ascii=False)

    # 2) Chunking (small and large)
    print("[*] Chunking text (small & large)...")
    chunks_small = chunk_text_chars(full_text, chunk_size=SMALL_CHUNK_SIZE, overlap=SMALL_CHUNK_OVERLAP)
    chunks_large = chunk_text_chars(full_text, chunk_size=LARGE_CHUNK_SIZE, overlap=LARGE_CHUNK_OVERLAP)
    print(f"[+] small: {len(chunks_small)} chunks, large: {len(chunks_large)} chunks")

    with open(CHUNKS_SPLIT_JSON, "w", encoding="utf8") as f:
        json.dump({"small": chunks_small, "large": chunks_large}, f, ensure_ascii=False)

    # Choose small by default for precision
    chunks = chunks_small
    with open(CHUNKS_JSON, "w", encoding="utf8") as f:
        json.dump({"used": "small", "chunks": chunks}, f, ensure_ascii=False)

    # 3) Embeddings (local)
    if not Path(EMBEDDINGS_NPY).exists():
        print("[*] Computing local embeddings for chunks...")
        emb_matrix = compute_local_embeddings(chunks, batch_size=32)
        np.save(EMBEDDINGS_NPY, emb_matrix)
        print(f"[+] Saved embeddings.npy shape {emb_matrix.shape}")
    else:
        emb_matrix = np.load(EMBEDDINGS_NPY)
        print(f"[+] Loaded embeddings.npy shape {emb_matrix.shape}")

    # 4) Build/load FAISS
    if not FAISS_INDEX_PATH.exists():
        print("[*] Building FAISS index...")
        index = build_faiss_index(emb_matrix)
        save_faiss_index(index, FAISS_INDEX_PATH)
        print(f"[+] Saved FAISS index to {FAISS_INDEX_PATH}")
    else:
        index = load_faiss_index(FAISS_INDEX_PATH)
        print(f"[+] Loaded FAISS index (ntotal={index.ntotal})")

    # Retrieval helpers using local embeddings for queries
    def embed_query_local(query: str) -> np.ndarray:
        qv = embed_model.encode([query], convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(qv)
        return qv

    def retrieve_topk_local(query: str, k: int = TOP_K):
        qv = embed_query_local(query)
        D, I = index.search(qv, k)
        hits = []
        for idx_i, score in zip(I[0], D[0]):
            if idx_i < 0 or idx_i >= len(chunks): 
                continue
            hits.append({"id": int(idx_i), "score": float(score), "chunk": chunks[int(idx_i)]})
        return hits

    # 5) RAG & Non-RAG with local generator
    def build_context_prompt_local(hits, question, per_chunk_chars=1500):
        parts = []
        for h in hits:
            txt = h["chunk"][:per_chunk_chars]
            parts.append(f"[chunk_id:{h['id']}]\n{txt}")
        context = "\n\n---\n".join(parts)
        prompt = (
            "You are a helpful assistant. Use ONLY the context below to answer the question. "
            "If the answer is not in the context, say 'Not enough information in the provided context.'\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer concisely and cite chunk ids."
        )
        return prompt

    def rag_answer_local(question: str, topk: int = 3):
        hits = retrieve_topk_local(question, k=topk)
        if not hits:
            return {"answer": "ERROR: no retrieval hits", "hits": []}
        prompt = build_context_prompt_local(hits, question)
        try:
            answer = generate_local(prompt)
            return {"answer": answer, "hits": hits}
        except Exception as e:
            return {"answer": f"ERROR: local generation: {type(e).__name__}: {e}", "hits": hits}

    def non_rag_local(question: str):
        try:
            answer = generate_local(question)
            return answer
        except Exception as e:
            return f"ERROR: local generation: {type(e).__name__}: {e}"

    # 6) Run sample questions and save responses
    QUESTIONS = [
        "Summarize the paper's main contribution in two sentences.",
        "What dataset(s) are used and what preprocessing steps are mentioned?",
        "Describe the model/architecture and key hyperparameters.",
        "What are the main experimental results and metrics reported?",
        "What limitations or future work does the paper mention?"
    ]

    results = []
    print("\n[*] Running RAG vs Non-RAG tests (local generator)...")
    for q in QUESTIONS:
        print("\n---\nQuestion:", q)
        r = rag_answer_local(q, topk=3)
        n = non_rag_local(q)
        results.append({
            "question": q,
            "rag_answer": r["answer"],
            "rag_hits": r["hits"],
            "non_rag_answer": n
        })
        print("RAG preview:", (r["answer"] or "")[:400])
        print("Non-RAG preview:", (n or "")[:400])

    with open(RESPONSES_JSON, "w", encoding="utf8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\nAll done. Files created/updated:")
    print(" -", CHUNKS_SPLIT_JSON)
    print(" -", EMBEDDINGS_NPY)
    print(" -", FAISS_INDEX_PATH)
    print(" -", RESPONSES_JSON)
    print(" -", COMPARISON_MD)

    # 8) Offer interactive mode
    def interactive_mode():
        print("\nInteractive mode: ask questions (type 'exit' to quit).")
        while True:
            q = input("\nQuestion> ").strip()
            if not q or q.lower() in ("exit", "quit"): break
            r = rag_answer_local(q, topk=3)
            print("\n--- RAG Answer ---\n", r["answer"])
            print("\nRAG hits (preview):")
            for h in r["hits"]:
                print(f" id:{h['id']} score:{h['score']:.3f} preview: {h['chunk'][:300].replace('\\n',' ')}")
            print("\n--- Non-RAG Answer ---\n", non_rag_local(q))

    # Launch interactive prompt for further testing
    interactive_mode()

if __name__ == "__main__":
    main_run()
