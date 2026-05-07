import os
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class SummarizeService:
    def __init__(self):
        self.llm = ChatOpenAI(model = 'gpt-4o-mini', temperature=0.3)
        self.prompt = ChatPromptTemplate.from_template("""You are an AI summarizer. Your task is to summmarize the input: {input} given by the user 
        & respond ONLY in a valid JSON object in the exact format. Give proper headings in summary if required to explain easily:
        {{
            "summary": "1/3 summary of the given text",
            "keyPoints": ["Point 1", "point 2", "point 3", "point 4", "point 5"]
        }}
        DONOT give any text outside the json object.""")
    
    def generate_summary(self, text : str) -> dict:
        chain = self.prompt | self.llm
        response = chain.invoke({'input': text})
        raw = response.content.strip()

       # Strip markdown fences if model adds them despite instructions
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]
        raw = raw.strip()

        return json.loads(raw)
        