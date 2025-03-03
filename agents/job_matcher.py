from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from utils.exceptions import JobMatcherJSONLoadsError, JobMatcherAnalysisNotFoundError, JobMatcherErrorSkillListEmpty
from database_handler import match_jobs
import firebase_admin
from firebase_admin import firestore, credentials
import datetime
from app_config import max_job_matches_num
class JobMatcher:
    async def run(self, messages: list) -> Dict[str, Any]:
        print("🚀 Matching potential jobs: ")
        cred = credentials.Certificate('../key.json')
        
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        try:
            content = messages[-1].get("content", "{}").replace("'", '"') #convert single quotes to double quotes to make it valid JSON
            analysis_results = json.loads(content)
        except json.JSONDecodeError as e:
            raise JobMatcherJSONLoadsError()
        
        skills_analysis = analysis_results.get("analysis_json", {})
        if not skills_analysis:
            raise JobMatcherAnalysisNotFoundError

        skills = skills_analysis.get("technical_skills", [])
        experience_level = skills_analysis.get("experience_level", "Intern")
        years_of_experience = int(skills_analysis.get("years_of_experience", "0"))
        if not isinstance(skills, list) or not skills:
            raise JobMatcherErrorSkillListEmpty

        if experience_level not in ["Intern", "Junior", "Mid", "Senior"]:
            print("Invalid experience level detected, defaulting to Intern.")
            experience_level = "Intern"

        print(f"Skills: {skills}, Experience Level: {experience_level}")

        matched_jobs = match_jobs(db, experience_level, skills, years_of_experience)
        if len(matched_jobs) == 0 : 
            raise
        return {
            "matched_jobs": matched_jobs,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
        }


    async def match_jobs(
        db: firestore.Client,
        experience_level: str,
        candidate_skills: List[str],
        years_of_experience: int
        ) -> List[Dict[str, Any]]:
        
        """
            Finds jobs that are best for given candidate and sorts them by candidate score
            Returns a list of dictionaries where each represents existing doc in jobs collection in the database that was matched wtih candidate.
            In addition to fields already existing for every doc in jobs collection it adds fields:
            required_skills_ratio: how many skills (that were specified as required in a job) candidate posseses compared to total number that was listed
            optional_skills_ratio: same as above but for skills specified as "optional" in job posting.
            candidate_skills_review: For now either 'Very Good' , or 'Appropriate' - an information to the LLM how rating system sees the candidate.
        """
        if len(candidate_skills) == 0:
            raise JobMatcherErrorSkillListEmpty
        
        jobs_ref = db.collection('jobs')\
                .where('experience_level', '==', experience_level)\
                .where('years_of_experience', '<=', years_of_experience)\
                .stream()
    
        matching_jobs = []
        
        for job in jobs_ref:
            job_data = job.to_dict()
            job_data['id'] = job.id  # Add document ID to the results
            
            #count how many of the job's required skills match the candidate's skills
            matching_skill_count = 0
            total_skill_count = 0
            for skill in job_data.get('required_skills', []):
                if skill in candidate_skills:
                    matching_skill_count += 1
                total_skill_count +=1 

            required_skills_ratio = round(matching_skill_count/total_skill_count, 2)
            job_data['required_skills_ratio'] = required_skills_ratio

            optional_matching_skill_count = 0
            optional_total_skill_count = 0
            for optional_skill in job_data.get('optional_skills', []):
                if skill in candidate_skills:
                    optional_matching_skill_count += 1
                optional_total_skill_count +=1 
            
            optional_skills_ratio = round(optional_matching_skill_count/optional_total_skill_count, 2)
            job_data['optional_skills_ratio'] = optional_skills_ratio

            if required_skills_ratio > 0.70 and (optional_skills_ratio > 0.3 or optional_matching_skill_count > 5):
                job_data['candidate_skills_review'] = "Very Good"
            else:
                job_data['candidate_skills_review'] = "Appropriate"

            #round result to integer, at least ~50% of required skills should be present
            if required_skills_ratio > 0.49: 
                matching_jobs.append(job_data)
        
        #sort the jobs first by required_skills_ratio and then by optional_skills_ratio
        matching_jobs.sort(key=lambda x: (x['required_skills_ratio'], x['optional_skills_ratio']), reverse=True)
        matching_jobs = matching_jobs[:max_job_matches_num]  #we take only best x matches (can be changed in app config)
        return matching_jobs
