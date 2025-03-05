#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime as dt
class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Evaluator Agent",
            instructions = """ Your task is:
            Evaluate how well candidate fits the job based on:
            - Required Skills match ratio.
            - Optional Skills match ratio
            - Candidate Skills review            - 
            - Education
            - Green Flags
            - Red Flags and concerns

            Data required for this task will be passed by a user.
            Provide a comprehensive evaluation report with detailed reasoning.
            """
        )

    async def run(self, messages: list, job_num: int) -> Dict[str, Any]:
        print("👓 Evaluating Candidate...")

        ctx = eval(messages[-1]["content"])
        if not ctx["analysis_results"]["analysis_json"] or not ctx["summarizer_output"]["structured_text"]:
            raise LookupError

        if len(ctx["job_matches"]["matched_jobs"]) == 0:
            res = "Candidate dind't match any existing jobs"
            return {
                "evaluator_report": res,
                "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
            }
        
        

        evaluator_prompt = f"""
            Data neccesary for this task is here:
                Matched Job details JSON
                    - Required Skills match ratio. (ratio of  skills cadidate listed that fitted the job description compared to total number of required skills listed in job requirements)
                    - Optional Skills match ratio. (the same as required skills ratio but for optional - but still valued skills)
                    - Candidate Skills review. (Wheather skills were rated as Very Good , or Appropriate, its only a suggestion - not a final score)  
                    data: {ctx["job_matches"]["matched_jobs"][job_num]}
                PDF Analization JSON: 
                    -all info about the candidate extracted from the pdf like expertise ares , key echievements, all (even not relevant to the job) skills listed by the candidate.
                    data: {ctx["analysis_results"]["analysis_json"]}
                For Green Flags and Red Flags try look through this summarization of the cv.
                    data: {ctx["summarizer_output"]["structured_text"]}
            """

        res = self.query_ollama(evaluator_prompt)

        return {
            "evaluator_report": res,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }
        
