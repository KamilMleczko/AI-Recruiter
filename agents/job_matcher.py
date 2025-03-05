from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from utils.exceptions import JobMatcherJSONLoadsError, JobMatcherAnalysisNotFoundError, JobMatcherErrorSkillListEmpty
import firebase_admin
from firebase_admin import firestore, credentials
import datetime as dt
from app_config import max_job_match_exp_num, max_job_match_skill_num
import os

class JobMatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name = "Job Matcher Agent",
            instructions = f""" Your task is to:
            Evaluate the similarity between candidate skills and skills mentioned in job description for IT job position. 
            
            User will provide you with a list of candidate skills and two job skill lists (one for required skills and one for optional skills).
            You should assess similarity score for both required and optional skills. Similarity score represents how closely candidate skills match job skills.
            Rememeber that you will have only one skill list of the candidate and two skill lists of the job, 
            so you will need to consider ONLY candidate skills that relate to the required job skills when evaluating required skills similarity .
            and then consider ONLY candidate skills that relate to the optional job skills when evaluating optional skills similarity.

            Skill scores should be represented by a natural number from 0 to 100 (0 meaning no similarity and 100 meaning 100% similarity).
            Remember that while some skills may not be represented by the same word, they might still be closely related (for example css and scss, or SQL and postgreSQL).
            Format the output as structured data (json) with the following structure:
            {{
                "required_skills_score": "value from 0 to 100",
                "optional_skills_score": "value from 0 to 100",
            }}
            """
        )
    async def run(self, messages: list) -> Dict[str, Any]:
        print("🚀 Matching potential jobs: ")
        
        key_path = os.path.join('.', 'key.json')
        cred = credentials.Certificate(key_path)
        
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        try:
            content = messages[-1].get("content", "{}").replace("'", '"') #converted single quotes to double quotes to make it valid JSON
            analysis_results = self.parse_json(content)
        except json.JSONDecodeError as e:
            raise JobMatcherJSONLoadsError(content)
        
        skills_analysis = analysis_results.get("analysis_json", {})
        if not skills_analysis:
            raise JobMatcherAnalysisNotFoundError

        #candidate tech skills
        skills = skills_analysis.get("technical_skills", [])
        if not isinstance(skills, list) or not skills:
            raise JobMatcherErrorSkillListEmpty
        
        #candidate expierience level 
        experience_level = skills_analysis.get("experience_level", "not_stated").lower()
        if experience_level not in ["intern", "junior", "mid", "senior", "not_stated"]:
            print("Invalid experience level detected, defaulting to not_stated.")
            experience_level = "not_stated"

        #candidate employment history
        employment_history = skills_analysis.get("employment_history", [])

        #if employment history is empty than it's probably for internship. 
        #if someone refered to himself as senior but employment history is empty that's still treated as an Intern
        if not isinstance(employment_history, list) or not employment_history:
            assesed_years_of_experience = 0
            assesed_experience_level = "intern"
        else:
            expierience_assesment = self.resolve_work_experience(experience_level, employment_history)
            assesed_years_of_experience = expierience_assesment['years_of_experience']
            assesed_experience_level = expierience_assesment['experience_level']

        print(f"Experience Level: {assesed_years_of_experience}, years of experience: {assesed_experience_level}")

        found_jobs = await self.filter_jobs_by_experience(db, assesed_experience_level, assesed_years_of_experience)
        if len(found_jobs) == 0 : 
            print("NO JOBS FOUND")
            found_jobs = [{"job_title": "No jobs found"}]
        else:
            matched_jobs = await self.match_jobs(db, found_jobs, skills)

        return {
            "matched_jobs": matched_jobs,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }


    async def resolve_work_experience(self, expierience_level: str, employment_history: List[Dict[str, Any]]) -> int:
        pass


    async def resolve_skill_score(self, candidate_skills: List[str], required_skills: List[str], optional_skills: List[str]) -> int:
        pass

    async def filter_jobs_by_experience(
        self,
        db: firestore.Client,
        experience_level: str,
        years_of_experience: int
        ) -> List[Dict[str, Any]]:
        
        """
            Finds jobs that match candidate experience level and years of experience, uses database.
        """

        jobs_ref = db.collection('jobs')\
                .where('experience_level', '==', experience_level)\
                .where('years_of_experience', '<=', years_of_experience)\
                .stream()
    
        print(f'Found {len(list(jobs_ref))} jobs from first query')
        matching_jobs = []
        
        for job in jobs_ref:
            job_data = job.to_dict()
            job_data['id'] = job.id  #Add doc id to the results
            
        
        #sort the jobs first by required_skills_ratio and then by optional_skills_ratio
        matching_jobs.sort(key=lambda x: (x['required_skills_ratio'], x['optional_skills_ratio']), reverse=True)
        #we take only best x matches to be later filtered via skill score, to best y matches ( both can be changed in app config)
        matching_jobs = matching_jobs[:max_job_match_exp_num]  
        return matching_jobs


    async def filter_jobs_by_skill_score(self,  experience_level: str, years_of_experience: int) -> List[Dict[str, Any]]:
        """ Filters jobs by skill score, does not use database"""
