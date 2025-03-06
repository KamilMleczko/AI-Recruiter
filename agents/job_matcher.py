from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from utils.exceptions import JobMatcherJSONLoadsError, JobMatcherAnalysisNotFoundError, JobMatcherErrorSkillListEmpty, JobMatcherInvalidWorkExp
import firebase_admin
from firebase_admin import firestore, credentials
import datetime as dt
from app_config import max_job_match_exp_num, max_job_match_skill_num
import os
import numpy as np
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
                "optional_skills_score": "value from 0 to 100"
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
            analysis_results = messages[-1].get("content", "{}")#converted single quotes to double quotes to make it valid JSON
        except json.JSONDecodeError as e:
            raise JobMatcherJSONLoadsError(analysis_results)
        
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
            expierience_assesment = await self.resolve_work_experience(experience_level, employment_history)
            assesed_years_of_experience = expierience_assesment['years_of_experience']
            assesed_experience_level = expierience_assesment['experience_level']

        print(f"Experience Level: {assesed_experience_level}, years of experience: {assesed_years_of_experience}")

        found_jobs = await self.filter_jobs_by_experience(db, assesed_experience_level, assesed_years_of_experience)
        if len(found_jobs) == 0 : 
            print("NO JOBS FOUND")
            # if no jobs were found we'll skip the skill filtering
            matched_jobs = [{"job_title": "No jobs found"}]
        else:
            #filter jobs by skill score
            matched_jobs = await self.filter_jobs_by_skill_score(skills, found_jobs)
        return {
            "matched_jobs": matched_jobs,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }


    async def resolve_work_experience(self, expierience_level: str, employment_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        years_of_internship = 0
        years_of_work = 0
    
        try:
            for employment in employment_history:
                print("Employment: ", employment)

                #check because llm model does not understand basic instructions like do not use anything but " intern " or " employee "
                if employment["position"].lower() not in ["intern", "employee"]:
                    employment["position"] = "intern"
                

                if employment["duration"] != "not_stated":
                    try:
                        employment["duration"] = int(employment["duration"])
                    except (ValueError, TypeError):
                        employment["duration"] = "not_stated"
                if employment["start_year"] != "not_stated":
                    try:
                        employment["start_year"] = int(employment["start_year"])
                    except (ValueError, TypeError):
                        employment["start_year"] = "not_stated"
                if employment["end_year"] != "not_stated":
                    try:
                        employment["end_year"] = int(employment["end_year"])
                    except (ValueError, TypeError):
                        employment["end_year"] = "not_stated"
                #end of IQ<10 CHECK

                if employment["position"].lower() == "intern":
                    if employment["duration"] == "not_stated":
                        end_year = 2025 if employment.get("end_year") == "not_stated" else int(employment.get("end_year", 2025))
                        start_year = 2025 if employment.get("start_year") == "not_stated" else int(employment.get("start_year", 2025))
                        duration = end_year - start_year
                        years_of_internship += duration
                    else:
                        years_of_internship += int(employment.get("duration", 1))
                elif employment["position"].lower() == "employee":
                    if employment["duration"] == "not_stated":
                        end_year = 2025 if employment.get("end_year") == "not_stated" else int(employment.get("end_year", 2025))
                        start_year = 2025 if employment.get("start_year") == "not_stated" else int(employment.get("start_year", 2025))
                        duration = end_year - start_year
                        years_of_work += duration
                    else:
                        years_of_work += int(employment.get("duration", 1))

            if  years_of_work == 0:
                exp_based_on_years = "intern"
            elif (3 > years_of_work > 0):
                exp_based_on_years = "junior"
            elif (6 > years_of_work >= 3):
                exp_based_on_years = "mid"
            elif (years_of_work >= 6):
                exp_based_on_years = "senior"
            else:
                exp_based_on_years == "unknown"

            rank_exp = {
                "not_stated": -1,
                "unknown": -1,
                "intern": 0,
                "junior": 2,
                "mid": 4,
                "senior": 7
            }
            
            if expierience_level == "not_stated" and exp_based_on_years != "unknown":
                assesed_experience_level = exp_based_on_years 
                assesed_years_of_experience = years_of_work + years_of_internship
            elif exp_based_on_years == "unknown" and expierience_level != "not_stated":
                assesed_experience_level = expierience_level
                assesed_years_of_experience = rank_exp[expierience_level] + years_of_internship
            else:
                if rank_exp[expierience_level] > rank_exp[exp_based_on_years]:
                    assesed_experience_level = expierience_level
                else:
                    assesed_experience_level = exp_based_on_years
                assesed_years_of_experience = years_of_work + years_of_internship 
                

        except Exception as e:
            raise JobMatcherInvalidWorkExp(employment_history, e)

        return {
            "experience_level": assesed_experience_level,
            "years_of_experience": assesed_years_of_experience
        }


    async def resolve_skill_score(self, candidate_skills: List[str], required_skills: List[str], optional_skills: List[str]) -> Dict[str, Any]:
        prompt = f""" 
            Evaluate candidate skill scores for required and optional skills.
            This is candidate skill list: {candidate_skills},
            this is required job skill list: {required_skills},
            this is optional job skill list: {optional_skills},
            Format the output as structured data (json) with the following structure:
            {{
                "required_skills_score": "value from 0 to 100",
                "optional_skills_score": "value from 0 to 100"
            }}
            Return ONLY json, nothing else.
        """

        
        tries = 0
        res = self.query_ollama(prompt)
        parsed_json = self.parse_json(res)
        while tries < 3:
            if parsed_json is None:
                print("JOB MATCHER: Error parsing JSON-like content. Retrying...")
                res = self.query_ollama(prompt)
                parsed_json = self.parse_json(res)
                tries += 1
            else:
                print(parsed_json)
                return parsed_json
        raise JobMatcherJSONLoadsError(res)



    async def filter_jobs_by_experience(
        self,
        db: firestore.Client,
        experience_level: str,
        years_of_experience: int
        ) -> List[Dict[str, Any]]:
        
        """
            Finds jobs that match candidate experience level and years of experience, uses database. This is first phase of filtering.
        """

        jobs_ref = db.collection('jobs')\
                .where('experience_level', '==', experience_level)\
                .where('years_of_experience', '<=', years_of_experience)\
                .stream()
    
        jobs_list = list(jobs_ref)
        print(f'Found {len(jobs_list)} jobs from first query')

        matching_jobs = []

        for job in jobs_list:
            job_data = job.to_dict()
            job_data['id'] = job.id  # Add doc id to the results
            matching_jobs.append(job_data)
        #we take only best x matches to be later filtered via skill score, to best y matches ( both can be changed in app config)
        top_matching_jobs = matching_jobs[:max_job_match_exp_num]  
        return top_matching_jobs


    async def filter_jobs_by_skill_score(self, candidate_skills: List[str], job_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ Filters jobs by skill score, does not use database. This is second phase of filtering."""
        for job in job_list:
            skill_score_assesment = await self.resolve_skill_score(candidate_skills, job["required_skills"], job["optional_skills"])
            job["required_skills_score"] = skill_score_assesment["required_skills_score"]
            job["optional_skills_score"] = skill_score_assesment["optional_skills_score"]
            print(f"Job {job['job_name']} has required skill score: {job['required_skills_score']} and optional skill score: {job['optional_skills_score']}")
        
        sorted_jobs = sorted(
        job_list,
        key=lambda job: (job["required_skills_score"], job["optional_skills_score"]),
        reverse=True
        )

        return sorted_jobs[:max_job_match_skill_num] #best y matches (can be changed in app config)
    