import os
import shutil
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_service import RAGService
from mcq_service import MCQService
from summarize_service import SummarizeService
from agent_service import AgentService

load_dotenv()

# ── Lifespan: init services once at startup ───────────────────
@asynccontextmanager
async def lifespan (app: FastAPI):
    app.state.rag = RAGService()
    app.state.mcq = MCQService()
    app.state.summarize = SummarizeService()
    app.state.agent = AgentService()
    yield

app = FastAPI(
    title='ai-study-assistant',
    description='Python app using rag pipeline.',
    version='1.0.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

class RequestQuestion(BaseModel):
    question: str
class UploadsResponse (BaseModel):
    message: str
    filename: str
    chunk_count: int
class AnswerResponse (BaseModel):
    question: str
    answer: str
    sources: list
class MCQRequest (BaseModel):
    topic: str
class SummarizeRequest (BaseModel):
    text: str
class AgentRequest (BaseModel):
    question:str

@app.get('/')
def root():
    return {'success': 'True', 'message': 'AI Study Assistant is Working!'}

@app.post('/upload', response_model=UploadsResponse)
async def upload_pdf (file: UploadFile= File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException (status_code=400, detail='Only PDF Files are allowed!')
    
    save_path = f'uploads/{file.filename}'
    with open(save_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = app.state.rag.ingest_pdf(save_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to upload pdf: {str(e)}')
    
    return UploadsResponse(
        message='PDF Uploaded and Embedded Successfully!',
        filename=file.filename,
        chunk_count=result['chunk_count']
    )

@app.post('/ask', response_model=AnswerResponse)
async def ask_ai (body: RequestQuestion):
    if not body.question.split():
        raise HTTPException(status_code=400, detail='Please ask a question')
    
    try:
        result = app.state.rag.query_rag(body.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to retrieve an answer: {str(e)}')
    
    return AnswerResponse(
        question= body.question,
        answer= result['answer'],
        sources= result['sources']
    )

@app.post('/generate_mcq')
def generate_mcq (body: MCQRequest):
    if not body.topic.strip():
        raise HTTPException(status_code=400, detail="Please provide a topic")
    try:
        response = app.state.mcq.generate(body.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to generate MCQs :{str(e)}')
    return response

@app.post('/summarize')
def summarize (body: SummarizeRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Please enter text to summarize.")
    try:
        result = app.state.summarize.generate_summary(body.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to Generate Summary: {str(e)}")
    return result

@app.post('/agent_ask')
def agent_ask (body: AgentRequest):
    if not body.question.split():
        raise HTTPException(status_code=400, detail="Please ask a question.")
    try:
        result = app.state.agent.create_agent(body.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer from agent:{str(e)}")
    return result

@app.delete('/reset')
def reset():
    app.state.rag.reset()
    return {'message': 'Vector store and history cleared.'}
