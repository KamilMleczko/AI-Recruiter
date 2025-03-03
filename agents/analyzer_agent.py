from typing import Dict, Any
from .base_agent import BaseAgent
import json
from utils.exceptions import AnalyzerJSONParseError
import datetime
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
        print("🔍 Analyzer: Analyzing candidate profile")

        extracted_data = eval(messages[-1]["content"])
        
        analysis_prompt = f"""
        Analyze this resume data and return a JSON object with the following structure:
        {{
            "experience_level": "Intern/Junior/Mid/Senior",
            "education": {{
                "level": "Bachelors/Masters/PhD",
                "field": "field of study"
            }},
            "years_of_experience": number,
            "technical_skills": ["skill1", "skill2"],
            "key_achievements": ["achievement1", "achievement2"],
            "expertise_areas": ["domain1", "domain2"]
        }}

        CV data:
        {extracted_data["structured_text"]}

        Return ONLY the JSON object, no other text.
        """

        res = self.query_ollama(analysis_prompt)
        try:
            parsed_json = self.parse_json(res)
        except json.JSONDecodeError:
            raise AnalyzerJSONParseError(res)

        

        return {
            "analysis_json": parsed_json,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
        }
