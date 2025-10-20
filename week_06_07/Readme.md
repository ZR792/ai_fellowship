# Week 06–07 — RAG & Multimodal AI Applications:

## Overview:
During **Week 6–7** of the Buildables AI Fellowship, I focused on exploring two major areas of advanced AI development:

1. **RAG (Retrieval-Augmented Generation) Mini Application**  
2. **Multimodal AI Application**

These projects helped me understand how **AI models can process, retrieve, and reason** over both **textual** and **visual** data — combining the power of **language models, embeddings, OCR, and vision models** in one workflow.

---

## Projects Overview:

### 1. RAG Mini Application:
The **RAG (Retrieval-Augmented Generation)** project was designed to improve the contextual understanding of language models by connecting them with relevant external data.  
It works by:
- **Splitting long documents** into manageable chunks.  
- **Creating embeddings** using `SentenceTransformers`.  
- **Storing embeddings** in a **FAISS vector database**.  
- **Retrieving top-matching text chunks** based on user queries.  
- **Generating AI-based answers** using retrieved context.

#### What I Learned:
- How **RAG pipelines** enhance LLMs with factual information.  
- How to use **FAISS** for semantic search.  
- How **embeddings** represent textual meaning numerically.  
- How to integrate retrieval + generation in Python.  

#### Future Improvements:
- Add **multi-document retrieval**.  
- Build a **simple UI** for query input/output.  
- Integrate **real dataset querying** (like research papers or product data).

---

### 2. Multimodal AI Application:
The **Multimodal App** combined **image, text, and document processing** capabilities into one system using the **Gemini API** and **Tesseract OCR**.

#### Core Functionalities:
- **Photo Analysis:** Generates captions and descriptions for images.  
- **Document OCR:** Extracts readable text from scanned images.  
- **Chart Understanding:** Performs reasoning on chart visuals.  
- **PDF Text Extraction:** Reads and processes long PDFs for AI summarization.  
- **RAG-like Demo:** Retrieves and summarizes sections of long documents.

#### Tools & Libraries:
- Python  
- Gemini Vision & Text APIs  
- Tesseract OCR  
- PyPDF2 / pdfplumber  
- FAISS + SentenceTransformers  
- Markdown output formatting  

#### What I Learned:
- The concept of **multimodality in AI** — how models handle multiple input types.  
- How to integrate **OCR** for real-world text extraction.  
- How **vision models** describe and reason about images.  
- Managing **long-context text** for summarization and search.  

#### Future Improvements:
- Add a **Streamlit interface** to upload and analyze files.  
- Use **better OCR preprocessing** for cleaner results.  
- Combine image + text results for **context-aware multimodal Q&A**.  
- Deploy as a **lightweight AI assistant web app**.

---

## Weekly Learning Summary:
This week gave me hands-on experience in:
- **RAG architectures and semantic retrieval.**  
- **Multimodal AI workflows** (text, image, and document data).  
- **Practical AI system integration** — combining multiple models and tools in one pipeline.  
- Handling **real-world AI tasks**, including OCR, embeddings, and vision-based reasoning.

---

## Reflection & Next Steps:
These two projects gave me a solid foundation for building **context-aware AI assistants** and **multimodal intelligent systems**.  
In the coming weeks, I plan to:
- Focus on **deployment (Streamlit/Gradio + APIs)**.  
- Enhance **retrieval quality** with better embeddings.  
- Experiment with **fine-tuning multimodal models**.

---

**Developed by:**  
 **Zainab Ramzan**  
*Software Engineering Student* | *Buildables AI Fellowship (Week 6–7)*  
