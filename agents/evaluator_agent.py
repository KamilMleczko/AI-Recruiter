#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime as dt
class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Evaluator Agent",
            instructions = """ Your task is:
            Evaluate  how well candidate fits the job based on:
            - Required Skills score (in % of  skills cadidate listed that fitted the job description compared to total number of required skills listed in job requirements)
            - Optional Skills score. (the same as required skills score but for optional - but still valued skills)   - 
            - Education
            - Green Flags
            - Red Flags and concerns

            Required Skills score and Optional skill score is already calculated and passed to you as part of the data , 
            so don't reevaluate it, just provide reasoning you can infer from the data.

            Use following rating scale:
            **Rating Scale**
                * 90-100%: Strong candidate with excellent fit for the job that posses many green flags
                * 80-89%: Good candidate some green flags but no concerns
                * 70-79%: Fair candidate that posses neither significant green flags nor red flags and concerns
                * 60-69%: Below average candidate with some red flags or concerns, lacking counterbalancing green flags
                * Below 50%: Weak candidate with major red flags or concerns that make them unsuitable for the job

            Data required for this task will be passed by a user.
            Provide a comprehensive evaluation report with detailed reasoning.
            Do not provide any other information, just the evaluation report - so no clear next steps or recommendations.
            """
        )

    async def run(self, messages: list, job_num: int) -> Dict[str, Any]:
        print("👓 Evaluating Candidate...")

        ctx = eval(messages[-1]["content"])
        if not ctx["analysis_results"]["analysis_json"] or not ctx["summarizer_output"]["structured_text"]:
            raise LookupError

        if len(ctx["job_matches"]["matched_jobs"]) == 0:
            print("Candidate dind't match any existing jobs")
            res = "Candidate dind't match any existing jobs"
            return {
                "evaluator_report": res,
                "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
            }
        
            
        print(ctx["job_matches"]["matched_jobs"][job_num])
        

        evaluator_prompt = f"""
            Data neccesary for this task is here:
                
            Matched Job details JSON: 
                data: {ctx["job_matches"]["matched_jobs"][job_num]}
            PDF Analization JSON: 
                -all info about the candidate extracted from the pdf like expertise ares , key achievements, all (even not relevant to the job) skills listed by the candidate.
                data: {ctx["analysis_results"]["analysis_json"]}
            For Green Flags and Red Flags try to look through this summarization of the cv.
                data: {ctx["summarizer_output"]["structured_text"]}
            """

        res = self.query_ollama(evaluator_prompt)
        print(res)
        return {
            "evaluator_report": res,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }
        
