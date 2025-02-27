from .base_agent import BaseAgent
from typing import Dict, Any

class JobMatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Job Matcher Agent",
            instructions = """ Match candidate profiles with job positions.
            Do it based on:
            - skills and qualifications match
            - expierience level
            - location preference

            Provide detailed reasoning, and compatibility scores.
            Return matches in json format with following fields: title, match_score, location.
            """
        )
    
    async def run(self, messages: list) -> Dict[str, Any]:
        print("🚀 Matching potential jobs: ")
        raise NotImplementedError
        #TODO