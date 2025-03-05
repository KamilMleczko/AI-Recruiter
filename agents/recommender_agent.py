#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime as dt
class RecommenderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Recommender Agent",
            instructions = """Generate final recommendations. 
            Consider Evaluations of every matched job.
            
            Out of all matched jobs pick the one you see as the best for the candidate, additionaly provide your confidence score
            Provide clear next steps and recommendations.
            Data needed will be provided by the user.
            """
        )
    
    async def run(self, messages: list) -> Dict[str, Any]:
        print("🚅 Generating final Recommendations: ")
        
        ctx = eval(messages[-1]["content"])

        recommender_prompt = f"""
            Data neccesary for this task is here:
                Evaluations for every job (list of JSON dictionaries, one for every matched job)
                    data: {ctx["candidate_to_jobs_evaluation"]}
            """

        res = self.query_ollama(recommender_prompt)
        
        return {
            "final_recommendation" : res,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }