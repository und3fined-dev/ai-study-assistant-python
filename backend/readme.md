# AI Study Assistant — Python

AI-powered study tool built with FastAPI, LangChain, and OpenAI.
Upload lecture notes or textbooks, ask questions, generate MCQs and get summaries.

## Features
- **RAG Q&A** — ask questions about any uploaded PDF and get relevant answers.
- **MCQ Generation** — generate 10 multiple choice questions on any topic.
- **Summarize** — paste any paragraphs to generate concise summary.
- **ReAct Agent** - ask any question and get answer either from uploaded docs, web or calculator. 

## Stack
- FastAPI + Uvicorn
- LangChain + OpenAI (gpt-4o-mini, text-embedding-3-small)
- ChromaDB (vector store)
- Pydantic (validation)
- create_react_agent (Choosing agent)

## Setup
```bash
cd backend
pip install -r requirements.txt
cp .env       # add your OPENAI_API_KEY
uvicorn main:app --reload
```

//Visit `http://localhost:8000/docs` for the interactive API.

## Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/upload` | Upload PDF → chunk → embed → store |
| POST | `/ask` | Question → RAG → answer + sources |
| POST | `/generate-mcq` | Topic → 10 MCQs as JSON |
| POST | `/agent_ask` | Query -> Tool choose -> Tool run -> Observe Result -> Output |
| DELETE | `/reset` | Clear vector store |

## Project Structure
```
backend/
├── main.py          # FastAPI routes
├── rag_service.py   # RAG pipeline
├── mcq_service.py   # MCQ generation
├── agent_service.py # Agent logic
└── requirements.txt
```