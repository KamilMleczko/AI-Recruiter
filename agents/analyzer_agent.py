from typing import Dict, Any
from .base_agent import BaseAgent

class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Analyzer",
            instructions="""Analyze candidate profiles and extract:
            1. Experience level (Intern/Junior/Mid/Senior) (as a string)
            2. Education (string)
            3. Years of experience (numeric)
            4. Technical skills (list of strings)
            5. Key achievements (list of strings)
            6. Main areas of expertise (list of strings)
            
            Format the output as structured data.""",
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        """Analyze the extracted resume data"""
        print("🔍 Analyzer: Analyzing candidate profile")
        raise NotImplementedError
        #extracted_data = eval(messages[-1]["content"])
        
        #TODO
