#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime
class RecommenderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Recommender Agent",
            instructions = """Generate final recommendations. 
            Consider:
            - Skills Analysis results
            - Job Matches
            - Candidate Evaluation results

            Provide clear next steps and recommendations.
            For every job matched list the job 
            and add your confidence score.
            """
        )
    
    async def run(self, messages: list) -> Dict[str, Any]:
        print("🚅 Generating final Recommendations: ")
        
        ctx = eval(messages[-1]["content"])
        recommendation  = self.query_ollama(str(ctx))
        return {
            "final_recommendation" : recommendation,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
        }