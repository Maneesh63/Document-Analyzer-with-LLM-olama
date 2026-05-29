# Document-Analyzer-with-LLM-olama

# 📄 PDF RAG Analyzer

A production-ready **Retrieval-Augmented Generation (RAG)** API built with **Django REST Framework** and **Ollama** — runs 100% locally, no paid APIs required.

Upload any PDF, ask questions in natural language, and get intelligent answers powered by local LLMs.

---

## 🚀 Features

- 📤 Upload PDF documents via REST API
- 🔍 Semantic search using vector embeddings
- 🤖 Local LLM inference via Ollama (no API key, no cost)
- 🧠 RAG pipeline with LangChain LCEL
- 🗃️ Vector storage with ChromaDB
- 📜 Query history tracking per document
- 🗑️ Clean document deletion (DB + vectors)
- 🔒 Fully private — all data stays on your machine

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django 5 + Django REST Framework |
| LLM | Ollama (`llama3.2`) |
| Embeddings | Ollama (`nomic-embed-text`) |
| RAG Framework | LangChain (LCEL) |
| Vector Database | ChromaDB |
| PDF Loader | PyPDF |
| Language | Python 3.11+ |

---

## 📋 Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- 4GB+ RAM (for LLM inference)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pdf-rag-analyzer.git
cd pdf-rag-analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama & Pull Models

```bash
# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull required models
ollama pull llama3.2           # LLM (~2 GB)
ollama pull nomic-embed-text   # Embeddings (~274 MB)
```

### 5. Environment Variables

Create a `.env` file in the root directory:

```env
# No API keys needed — Ollama runs locally!
OLLAMA_BASE_URL=http://localhost:11434
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Start the Server

```bash
# Terminal 1 — make sure Ollama is running
ollama serve       # skip if already running (Mac app)

# Terminal 2 — start Django
python manage.py runserver
```

---

## 📡 API Endpoints

### Upload PDF
```http
POST /api/docs/upload/
Content-Type: multipart/form-data

Body: file=<your-pdf-file>
```

**Response:**
```json
{
    "id": "uuid",
    "filename": "resume.pdf",
    "status": "ready",
    "total_chunks": 12,
    "created_at": "2025-01-01T00:00:00Z"
}
```

---

### Ask a Question
```http
POST /api/docs/<doc_id>/query/
Content-Type: application/json

{
    "question": "Who is Maneesh?"
}
```

**Response:**
```json
{
    "question": "Who is Maneesh?",
    "answer": "Maneesh M is a Backend Developer with over 10 months of experience building scalable web applications using Django and REST APIs. His key skills include Python, SQL, Django REST Framework, and cloud services like AWS."
}
```

---

### List All Documents
```http
GET /api/docs/
```

---

### Delete Document
```http
DELETE /api/docs/<doc_id>/delete/
```

---

### Query History
```http
GET /api/docs/<doc_id>/history/
```

---

## 🗂️ Project Structure

```
pdf-rag-analyzer/
│
├── manage.py
├── requirements.txt
├── .env
│
├── rag_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── documents/
│   ├── models.py          # Document & QueryHistory models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   └── rag_pipeline.py    # RAG logic (LangChain + Ollama + Chroma)
│
├── media/
│   └── pdfs/              # Uploaded PDF files
│
└── chroma_db/             # Vector embeddings store
```

---

## 🧠 How It Works

```
1. UPLOAD
   PDF File → PyPDFLoader → Text Chunks → nomic-embed-text → ChromaDB

2. QUERY
   Question → nomic-embed-text → Similarity Search → Top 3 Chunks
   Chunks + Question → llama3.2 → Detailed Answer
```

The system uses **LCEL (LangChain Expression Language)** for the RAG chain:

```python
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | ChatOllama(model="llama3.2")
    | StrOutputParser()
)
```

---

## 📦 requirements.txt

```
django==5.0.6
djangorestframework==3.15.2
python-dotenv==1.0.1
langchain==0.3.22
langchain-core==0.3.56
langchain-community==0.3.20
langchain-text-splitters==0.3.7
langchain-ollama
langchain-chroma==1.1.0
chromadb>=0.4.0,<0.7.0
pypdf==4.3.1
```

---

## 🔧 Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `LLM_MODEL` | `llama3.2` | Ollama LLM model |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `3` | Chunks retrieved per query |

---

## 🐛 Troubleshooting

**Ollama connection error:**
```bash
# Check if Ollama is running
curl http://localhost:11434
# Should return: Ollama is running
```

**Model not found:**
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama list   # verify both appear
```

**ChromaDB error on re-indexing:**
```bash
# Delete the chroma_db folder and re-upload
rm -rf chroma_db/
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License — feel free to use this project for personal or commercial purposes.

---

## 👨‍💻 Author

**Maneesh M**
- GitHub: [@Maneesh63](https://github.com/Maneesh63)
- LinkedIn: [maneesh63](https://linkedin.com/in/maneesh63/)
- Email: maneeshmofficial@gmail.com

---

> Built with ❤️ using Django, LangChain, Ollama, and ChromaDB
