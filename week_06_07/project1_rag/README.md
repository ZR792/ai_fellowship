#  Local Retrieval-Augmented Generation (RAG) vs Non-RAG System:

This project implements and compares two text generation pipelines **without using any external API or internet connection**.  
It demonstrates how a **local RAG (Retrieval-Augmented Generation)** pipeline improves the accuracy and relevance of responses compared to a **Non-RAG baseline**.

---

##  Project Overview:

The goal of this project is to show how **retrieving relevant document chunks** before generation leads to **better and contextually grounded answers**.

###  Features:
- ✅ **PDF Extraction** — Reads and extracts text from a local PDF.
- ✅ **Text Chunking** — Splits the extracted text into smaller, meaningful segments.
- ✅ **Embeddings** — Converts text chunks into numerical vectors.
- ✅ **Vector Database (FAISS)** — Stores embeddings for efficient similarity search.
- ✅ **RAG Pipeline** — Retrieves the most relevant chunks and generates contextual answers.
- ✅ **Non-RAG Baseline** — Generates responses without using document context.
- ✅ **Comparison Analysis** — Evaluates accuracy, relevance, and factual grounding.

---

## 🗂️ Project Structure

````
project1-rag/
│
├── rag_system.py              # Core RAG pipeline implementation
├── sample.pdf                 # Input PDF document for testing
├── chunks.json                # Stored chunks after processing
├── embeddings.npy             # Numerical vector embeddings
├── faiss.index                # FAISS vector index (for similarity search)
├── responses.json             # Model outputs from RAG and Non-RAG runs
├── comparison_analysis.md     # Detailed comparison analysis
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation (this file)
````

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment:
``
python -m venv rag_env
``
### 2️⃣ Activate Environment:

- Windows:

``
task6_7\Scripts\activate
``

### 3️⃣ Install Dependencies:
``
pip install -r project1-rag/requirements.txt
``

### ▶️ How to Run:

-  Step 1: Run the RAG System:
``
python project1-rag/rag_system.py
``

- The program will extract text from sample.pdf.

- It will create chunks, generate embeddings, and build the FAISS vector index.

- You’ll then enter interactive mode to ask questions.

### Example:
``
Interactive mode: ask questions (type 'exit' to quit).

Question> What is the paper mainly about?
``

* You’ll receive both:

- A RAG answer (contextual, document-based)

- A Non-RAG answer (model-only baseline)

- All responses will be saved in responses.json.

###  Key Learnings:

- RAG ensures factual accuracy by grounding answers in document data.
- Chunking and embeddings form the foundation of effective retrieval.
- FAISS allows fast, scalable similarity search locally.
- Non-RAG outputs highlight the limitations of models without context.

###  Conclusion:

This project successfully demonstrates a local RAG pipeline that processes a document from PDF to contextual Q&A —
highlighting how retrieval improves quality over a simple non-retrieval system.

