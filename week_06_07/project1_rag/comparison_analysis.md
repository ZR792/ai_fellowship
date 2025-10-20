# Comparison Analysis: RAG vs Non-RAG Pipeline

## 📘 Overview

This document compares the **Retrieval-Augmented Generation (RAG)** pipeline and a **Non-RAG (Direct LLM)** approach on the same PDF dataset.  
Both systems use the same model (`gemini-2.5-flash`), but the difference lies in **how context is provided** to the model.

---

##  RAG Pipeline Overview:

**RAG (Retrieval-Augmented Generation)** enhances responses by retrieving relevant document chunks before generating the final answer.

###  Key Steps:
1. **PDF Extraction:** The system extracts text from `sample.pdf` using `PyPDF2`.
2. **Chunking:** The extracted text is split into manageable sections for better embedding.
3. **Embeddings:** Each chunk is converted into a numerical vector using Gemini embeddings.
4. **Vector Database:** FAISS stores these embeddings for fast similarity search.
5. **Retrieval:** When a user asks a question, the most relevant chunks are retrieved.
6. **Generation:** The retrieved context is passed to the model for answer generation.

### ✅ Advantages:
- Provides **accurate and context-aware** answers.
- Capable of handling **domain-specific** queries using real document data.
- Reduces hallucinations since the model relies on retrieved evidence.

### ⚠️ Limitations:
- Requires additional preprocessing (chunking, embedding, FAISS index).
- More compute and memory usage.
- Accuracy depends on **retrieval quality** and **chunk size**.

---

## 💬 Non-RAG Pipeline Overview

**Non-RAG** directly queries the LLM without any retrieval mechanism.

###  Key Steps:
1. User input is directly sent to the model.
2. Model generates a response **based only on pre-trained knowledge**, not the PDF.

### ✅ Advantages:
- Simple and fast (no preprocessing or embeddings).
- Good for **general knowledge** queries.

### ⚠️ Limitations:
- Often produces **irrelevant or hallucinated answers** for specific documents.
- Does not reference uploaded PDFs.
- Poor factual accuracy on unseen data.

---

## 📊 Comparative Results:

| Feature / Aspect | RAG Pipeline | Non-RAG Pipeline |
|------------------|--------------|------------------|
| **Data Source** | Uses document context | Uses model’s internal knowledge |
| **Accuracy** | High (context-driven) | Low to medium |
| **Relevance to PDF** | Very high | Often irrelevant |
| **Computation Cost** | Moderate to high | Low |
| **Ease of Setup** | More complex | Very simple |
| **Hallucinations** | Reduced | Frequent |
| **Ideal Use Case** | Document QA, research summaries | General chat, idea generation |

---

##  Example Comparison (From Execution):

| Question | RAG Answer Summary | Non-RAG Answer Summary |
|-----------|--------------------|-------------------------|
| *Which ablation experiment had the largest impact?* | Cited numeric experiment details | Random short phrase ("a syringe") |
| *Do authors claim state-of-the-art performance?* | “No” – factual and grounded | Irrelevant response (“the symphony”) |
| *Find the main contribution sentence.* | Pulled reference IDs and partial citation | Generic answer (“the main contribution”) |

### 🔍 Observation
- RAG responses are **text-heavy, technical, and evidence-based**.
- Non-RAG responses are **short, vague, and off-topic**.

---

## 🧩 Evaluation Criteria (50 Points)

| Criteria | Points |
|-----------|---------|
| PDF extraction works correctly | 8 |
| Chunking and embeddings implemented | 8 |
| Vector database functioning | 8 |
| RAG pipeline works end-to-end | 10 |
| Comparison analysis (RAG vs Non-RAG) | 10 |
| Code quality and documentation | 6 |

---

## 🏁 Conclusion

The **RAG pipeline** provides significantly better, context-aware answers using information retrieved from the uploaded PDF.  
While the **Non-RAG model** performs adequately for general queries, it fails to give meaningful or document-specific answers.

> ✅ **Final Verdict:**  
> For any domain-specific, factual, or document-based tasks — **RAG is the superior approach**.

---

**Author:** *Zainab Ramzan*  
**Project:** *RAG System Implementation (AI Fellowship Week 6 & 7 Task)*  
**Date:** *17th October, 2025*
