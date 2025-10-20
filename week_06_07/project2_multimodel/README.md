# Multimodal AI Application — Vision-Enabled Document & Image Analyzer

### Project Overview:
This project is part of **Week 6–7 Assignment (Buildables AI Fellowship)** and focuses on building a **Multimodal AI system** — an intelligent tool that combines **text and image understanding**.  
The goal is to demonstrate how AI can process **visual data (images, charts, documents)** along with **text** to extract meaningful information and perform reasoning.

This project uses **Gemini API (or local fallback models)** to analyze multiple input types and generate insights from them.

---

## Objective:
To build a **multimodal AI application** capable of:
1. Reading and analyzing images (photo, document, chart).
2. Extracting text from scanned or printed documents using OCR.
3. Interpreting visual content (charts, images).
4. Processing long text documents (PDFs) for contextual understanding.
5. Combining these abilities to solve a **real-world use case**.

---

## Use Case: “Document Analyzer + Vision Assistant”:
The multimodal system serves as a **document and image understanding assistant** — it can:
- **Read scanned reports or invoices** (OCR extraction).  
- **Describe visual scenes** from photos (image captioning).  
- **Interpret charts and graphs** (visual reasoning).  
- **Process long text PDFs** such as research papers or reports, and retrieve context.  

This is useful for professionals, students, or researchers who deal with mixed data formats — allowing them to understand visual and textual content together.

---

## Features Implemented:
| Feature | Description |
|----------|--------------|
| **Image Analysis** | Generates captions and semantic understanding from a photo (`photo.jpg`). |
| **Document OCR** | Extracts printed or scanned text from an image (`document.png`) using **Tesseract OCR**. |
| **Chart Interpretation** | Reads chart/graph images (`chart.png`) and provides an analytical summary. |
| **Long-context Text Understanding** | Extracts and summarizes key sections from a large PDF file (`long_text.pdf`). |
| **Multimodal Reasoning** | Combines text + visual information to provide meaningful insights. |
| **Structured Output** | Saves results (image captions, OCR text, extracted summaries) to `outputs/example_outputs.md`. |

---

##  Tech Stack:
| Category | Tools / Libraries |
|-----------|------------------|
| **Language** | Python 3.10+ |
| **AI/ML Models** | Gemini API (Vision Model), SentenceTransformers (fallback embeddings) |
| **OCR Engine** | Tesseract OCR |
| **PDF Processing** | PyPDF2, pdfplumber |
| **Vector DB (optional)** | FAISS (for text embeddings) |
| **Others** | Pillow, pytesseract, torch, numpy |

---

## 📂 Folder Structure
````
project2_multimodel/
├── gemini_utils.py                 # Handles Gemini / local model logic
├── multimodal_app.py               # Main script to run analysis
├── images/
│ ├── photo.jpg
│ ├── document.png
│ └── chart.png
├── long_text.pdf                   # Large text PDF (e.g., research paper)
├── outputs/
│ └── example_outputs.md            # Generated results (captions, OCR text, summaries)
├── requirements.txt
└── README.md
````

---

## ⚙️ How to Run
1. **Install dependencies**
``
   pip install -r requirements.txt
   ``
2. Install Tesseract OCR
Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)

3. Run the multimodal script
``
python project2_multimodel/multimodal_app.py
``

### Key Learnings:

- Hands-on experience integrating vision + text AI models.
- Understanding OCR pipelines with Tesseract.
- Experience with PDF extraction and long-context understanding.
- Familiarity with FAISS and embeddings for semantic retrieval.
- Demonstrated how multimodal AI can bridge textual and visual content for real-world tasks.

### Challenges Faced:

- OCR quality varied depending on image clarity and font style.
- Extracting clean text from complex PDF layouts required experimentation with both PyPDF2 and pdfplumber.
- Chunking and retrieval needed tuning for better context results.
- Large models (like Gemini) required careful prompt management to reduce hallucination.

### Conclusion:

This multimodal AI project demonstrates how modern AI systems can handle multiple types of data — images, documents, charts, and text — to perform intelligent analysis and reasoning.
