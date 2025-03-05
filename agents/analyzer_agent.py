from typing import Dict, Any
from .base_agent import BaseAgent
import json
from utils.exceptions import AnalyzerJSONParseError
import datetime as dt
class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Analyzer",
            instructions="""Analyze candidate profiles based on cv data inputed by the user and extract:
            1. Experience level (intern/junior/mid/senior) (as a string).
            2. Education 
            3. History of employment
            4. Technical skills (list of strings)
            5. Key achievements (list of strings)
            6. Main areas of expertise (list of strings)
            
            Format the output as structured data (json).""",
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        print("🔍 Analyzer: Analyzing candidate profile")

        extracted_data = eval(messages[-1]["content"])
        print(extracted_data["structured_text"])
        analysis_prompt = f"""
        Analyze this resume data and return a JSON object with the following structure (slashes "/" mean an alternative you can only choose on of the listed options):
        {{
            "experience_level": "intern/junior/mid/senior/not_stated",
            "education": {{
                "level": "Bachelors/Masters/PhD",
                "field": "field of study"
            }},
            "employment_history": [
                {{
                    "start_year": year,
                    "end_year": year,
                    "position": "intern/employee",
                    "title": "job title",
                    "company": "company name"
                }},
                {{
                    "start_year": year/not_stated,
                    "end_year": year/not_stated,
                    "position": "intern/employee",
                    "title": "job title2",
                    "company": "company name2"
                }}

            ],
            "technical_skills": ["skill1", "skill2"],
            "key_achievements": ["achievement1", "achievement2"],
            "expertise_areas": ["domain1", "domain2"]
        }}

        Ad. expierience_level:
        If no expierience level is stated, in expierience_level field (in json you create) use "not_stated"
        For expierience_level use only one of those 4 strings: intern/junior/mid/senior/not_stated, you can't use string like "junior/mid". 
        If in cv data there are mentioned multiple expierience levels across jobs, then in json add ONLY the highest expierience level (example: first job: Junior, second Job: Mid, you add ONLY Mid).
        Expierience level and all skills should be in lowercase.

        Ad. employment_history:
        Employment history will be listed in the cv data, remeber that it is a list of several jobs.
        You can add to json ONLY the year itself (no months or days).
        If end year is not stated in cv data or stated as "current", then in json set end_year to 2025 if it was the most recent job, otherwise set end_year to 'not_stated'.
        If start year is not stated in cv data, then in json set start_year to 'not_stated'.
        Rememember that in cv data alongside work expierience,
        there can also be listed education (also with years specified) - DO NOT treat that as employment history.

        CV data:
        {extracted_data["structured_text"]}

        Return ONLY the JSON object, no other text.
        """

        res = self.query_ollama(analysis_prompt)
        try:
            parsed_json = self.parse_json(res)
        except Exception as e:
            raise AnalyzerJSONParseError(res,e)

        
        print(parsed_json)

        return {
            "analysis_json": parsed_json,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }
