import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

class RAGService:
    load_dotenv()
    CHROMA_DIR = '../chroma_db'
    UPLOAD_DIR = '../uploads'
    EMBEDDINGS_MODEL = 'text-embedding-3-small'

    def __init__(self):
        os.makedirs(self.CHROMA_DIR, exist_ok=True)
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

        self.embeddings = OpenAIEmbeddings(model = self.EMBEDDINGS_MODEL)
        self.llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.4)
        self.rag_prompt = ChatPromptTemplate.from_template("""
        You are a helpful study assistant. Answer the question using ONLY the provided context. If the answer is not in the context, clearly say
        "This information is not in the document." Do not make up information. Be concise and clear.
        Context: {context}
        Question: {input}
        Answer:""")

    def ingest_pdf (self, pdf_path : str) -> dict:

        #Upload PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        #Split into Chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50,
            length_function = len
        )
        chunks = splitter.split_documents(pages)

        #Embed + store
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding = self.embeddings,
            persist_directory= self.CHROMA_DIR
        )
        return {
            'chunk_count': vector_store._collection.count(),
            'page_count': len(pages)
        }

    def get_qa_chain (self):    
        vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.CHROMA_DIR
        )
        retriever = vector_store.as_retriever(
            search_type = 'similarity',
            kwargs={'k': 4}
        )
        docs_chain = create_stuff_documents_chain(self.llm, self.rag_prompt)
        qa_chain = create_retrieval_chain(retriever, docs_chain)
        return qa_chain

    def query_rag (self, question : str) -> dict:
        chain = self.get_qa_chain()
        result = chain.invoke ({'input': question})

        sources = []
        for doc in result['context']:
            sources.append({
                'page':    doc.metadata.get('page', '?'),
                'preview': doc.page_content[:200].replace('\n', ' ')
            })

        return {
            'answer':  result['answer'],
            'sources': sources
        }
    
    def reset(self):
        shutil.rmtree(self.CHROMA_DIR, ignore_errors=True)
        os.makedirs(self.CHROMA_DIR, exist_ok=True)
        shutil.rmtree(self.UPLOAD_DIR, ignore_errors=True)
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)