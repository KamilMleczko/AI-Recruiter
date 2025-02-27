#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime
class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Evaluator Agent",
            instructions = """ Evaluate how well candidate fits the job based on:
            - Skills match percentage.
            - Expierience match percentage
            - Education
            - Cultural Fit Indicators.
            - Green Flags
            - Red Flags and concerns.
            
            Provide a comprehensive evaluation report.
            """
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        print("👓 Evaluating Candidate...")

        ctx = eval(messages[-1]["content"])
        res = self.query_ollama(str(ctx))

        return {
            "evaluator_report": res,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
        }
        
