---
title: AI Study Assistant
emoji: 📚
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: frontend/app.py
pinned: false
---
# 📚 AI Study Assistant

> Ask questions, generate quizzes, and master any subject — just upload your notes.

An intelligent study companion powered by a RAG (Retrieval-Augmented Generation) pipeline. Upload your course PDFs, chat with them in natural language, generate MCQs on any topic, and summarize any text — all in one clean interface.

---

## ✨ Features

- **📄 PDF Upload & Indexing** — Upload lecture notes or textbook chapters; they're chunked, embedded, and stored in a local vector database
- **💬 RAG-Powered Chat** — Ask questions grounded in your uploaded documents; the assistant retrieves relevant context before answering
- **🧠 MCQ Generation** — Enter any topic and get 10 multiple choice questions with answers and explanations
- **🔍 Text Summarization** — Paste any text and get a concise summary with key points
- **🗑️ Reset** — Clear the vector store and start fresh anytime

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector Store | ChromaDB |
| RAG Pipeline | LangChain |
| PDF Parsing | PyPDFLoader |

---

## 📁 Folder Structure

```
ai-study-assistant-python/
├── frontend/
│   └── app.py                  # Streamlit UI
├── backend/
│   ├── main.py                 # FastAPI routes
│   ├── rag_service.py          # PDF ingestion + RAG query
│   ├── mcq_service.py          # MCQ generation via LLM
│   ├── summarize_service.py    # Text summarization via LLM
│   |── agent_service.py        # LangChain agent (optional)
|   └── .env                    # API keys (not committed)

├── uploads/                    # Uploaded PDFs (auto-created)
├── chroma_db/                  # Vector store (auto-created)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/und3fined-dev/ai-study-assistant-python
cd ai-study-assistant-python
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the backend/ of `ai-study-assistant-python/`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Running the App

You need to run **two terminals** — one for the backend, one for the frontend.

### Terminal 1 — Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

The API will be live at: `http://127.0.0.1:8000`  
Swagger docs at: `http://127.0.0.1:8000/docs`

### Terminal 2 — Start the Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

The app will open in your browser at: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload and index a PDF |
| `POST` | `/ask` | Ask a question (RAG) |
| `POST` | `/generate_mcq` | Generate MCQs on a topic |
| `POST` | `/summarize` | Summarize text |
| `DELETE` | `/reset` | Clear vector store and uploads |

---

## 📋 Requirements

```
fastapi
uvicorn
streamlit
requests
python-dotenv
langchain
langchain-openai
langchain-community
langchain-chroma
langchain-text-splitters
chromadb
pypdf
python-multipart
```

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key from [platform.openai.com](https://platform.openai.com) |

Never commit your `.env` file. Make sure it's in your `.gitignore`.

---

## 👤 Author

**Eashal** — [@und3fined-dev](https://github.com/und3fined-dev)
