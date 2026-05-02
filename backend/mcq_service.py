from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

class MCQService:
    def __init__(self):
        self.llm = ChatOpenAI(model = 'gpt-4o-mini', temperature=0.7)
        self.prompt = ChatPromptTemplate.from_template("""Generate exactly 10 multiple choice questions about: {topic}
        Rules:
        - Each question has exactly 4 options labeled A, B, C, D
        - Only one option is correct
        - Questions should test genuine understanding, not just memorisation
        - Vary difficulty: 2 easy, 2 medium, 1 hard
                                                       
        Return ONLY valid JSON. No explanation, no markdown, no backticks.
        Use exactly this structure:
        {{
            "topic": "{topic}",
            "questions": [
                {{
                    "id": 1,
                    "question": "Question text here?",
                    "options": {{
                        "A": "Option A text",
                        "B": "Option B text",
                        "C": "Option C text",
                        "D": "Option D text"
                }},
                "correct_answer": "A",
                "explanation": "Brief explanation of why A is correct."
                }}
            ]
        }}""")

    def generate (self, topic: str) -> dict:
        chain = self.prompt | self.llm
        response = chain.invoke({'topic': topic})
        raw = response.content.strip()

        # Strip markdown fences if model adds them despite instructions
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]
        raw = raw.strip()

        return json.loads(raw)