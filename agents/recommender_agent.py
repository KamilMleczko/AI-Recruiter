#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime as dt
class RecommenderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Recommender Agent",
            instructions = """Given 3 jobs macthed to the candidate and  their evaluations, generate final recommendation. 
            Out of all matched jobs pick the ONE you see as the best fit for the candidate based on data provided by the user.
            List picked job details (like position, salary , localisation etc.) and provide clear reasoning why you picked this job as the best.
            Provide clear next steps and recommendations .
            Data needed will be provided by the user.
            """
        )
    
    async def run(self, messages: list) -> Dict[str, Any]:
        print("🚅 Generating final Recommendations: ")
        
        ctx = eval(messages[-1]["content"])

        recommender_prompt = f"""
            Generate final recommendation. 
            Out of all matched jobs pick the ONE you see as the best for the candidate.
            
            Data neccesary for this task is here:            
                    Jobs Matched to the candidate details (list of JSON dictionaries, one for every matched job) : {ctx["job_matches"]["matched_jobs"]}
                    Evaluations for every matched job (all evaluations refer to the same candidate , one for every job he matched) : data: {ctx["candidate_to_jobs_evaluation"]}   
            """
        res = self.query_ollama(recommender_prompt)
        print(res)
        return {
            "final_recommendation" : res,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }