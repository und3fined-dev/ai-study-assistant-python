# import os
# import json
# import numexpr

# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_classic.agents import create_react_agent, AgentExecutor
# from langchain.tools import tool
# from langchain_classic import hub
# from langchain_chroma import Chroma
# from langchain_community.tools import DuckDuckGoSearchRun

# load_dotenv()
# CHROMA_DIR = './chroma_db'

# ##### Tool 1 ######
# @tool
# def web_search (query: str) -> str:
#     """Search the web for current information, recent news, or anything not likely to be in a local document. 
#     Use this for questions about recent events, general knowledge, or up-to-date facts."""

#     search = DuckDuckGoSearchRun
#     try:
#         result = search.run(query)
#     except Exception as e:
#         return f"Serach failed: {str(e)}"
#     return result

# #### Tool 2 #####
# @tool
# def PDFSearch (query: str) -> str:
#     """Search the uploaded study material and PDF documents for information. Use this for questions about the specific 
#     document content, lecture notes, textbook material, or anything that would be in a student's study files."""
#     try:
#         vector_store = Chroma(
#             embedding_function=OpenAIEmbeddings(model = 'text-embedding-3-small'),
#             persist_directory=CHROMA_DIR
#         )
#         retriever = vector_store.as_retriever(
#             search_type = "similarity",
#             kwargs={'k': 4}
#         )
#         docs = retriever.invoke(query)

#         if not docs:
#             return "No relevant content found in the knowledge base."
#         results = []
#         for i, doc in enumerate(docs, 1):
#             page = doc.metadata.get('page', '?')
#             results.append(f"[Chunk {i} — Page {page}]\n{doc.page_content}")
#         return '\n\n'.join(results)

#     except Exception as e:
#         return f"Knowledge base search failed: {str(e)}"
    
# ##### Tool 3 #######
# @tool
# def calculator (expression :str) -> str:
#     """Evaluate a mathematical expression. Use this for any arithmetic, percentage calculations, or numerical reasoning. 
#     Input must be a valid Python math expression like '(23 * 4) / 2' or '0.15 * 250'. Do not pass text — only math expressions."""

#     try:
#         result = numexpr.evaluate(expression).item()
#     except Exception as e:
#         return f"Calculation Failed: {str(e)}"
#     return f"{expression} = {result}"


# class AgentService:
#     def __init__(self):
#         self.llm = ChatOpenAI(model = 'gpt-4o-mini', temperature=0)
#         self.react_prompt = hub.pull('hwchase17/react')
#         self.tools = [web_search, PDFSearch, calculator]
   
#     ##### Create Agent ######
#     def create_agent(self, query:str) -> dict:
#         agent = create_react_agent(
#             llm=self.llm,
#             prompt=self.react_prompt,
#             tools=self.tools
#         )
#         agent_executor = AgentExecutor(
#             agent = agent,
#             tools = self.tools,
#             verbose = True,
#             max_iterations = 6,
#             handle_parsing_errors = True
#         )
#         response = agent_executor.invoke({'input': query})
#         return {
#             'question': query,
#             'answer': response['output']
#         }
