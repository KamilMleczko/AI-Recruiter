import firebase_admin
from firebase_admin import firestore, credentials
from typing import List, Dict, Any


def add_example_job_to_database(db):
   
    job_data = {
        'company_name': 'Acme Corporation',
        'job_name': 'Software Engineer',
        'location': 'San Francisco, CA',
        'experience_level': 'Mid',
        'required_skills': ['Python', 'JavaScript', 'Git', 'REST APIs'],
        'optional_skills': ['React', 'Docker', 'AWS', 'CI/CD'],
        'salary': '$120,000 - $150,000',
        'benefits': 'Health, dental, and vision insurance, 401(k) matching, unlimited PTO, remote work options, and professional development budget.',
        'description': 'We are looking for a talented Software Engineer to join our growing team. The ideal candidate will have experience with Python, JavaScript, and cloud technologies.'
    }
    job_ref = db.collection('jobs').add(job_data)
    
    return job_ref[1].id


def add_job_to_database(
    db: firestore.Client,
    company_name: str,
    job_name: str,
    location: str,
    experience_level: str,
    required_skills: List[str],
    optional_skills: List[str],
    salary: str,
    benefits: str,
    description: str

) -> str:
    if not isinstance(company_name, str):
        raise TypeError("company_name must be a string")
    if not isinstance(job_name, str):
        raise TypeError("job_name must be a string")
    if not isinstance(location, str):
        raise TypeError("location must be a string")
    if not isinstance(experience_level, str):
        raise TypeError("experience_level must be a string")
    if not isinstance(salary, str):
        raise TypeError("salary must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")
    if not isinstance(required_skills, list):
        raise TypeError("required_skills must be a list")
    if not isinstance(optional_skills, list):
        raise TypeError("optional_skills must be a list")
    if not isinstance(benefits, str):
        raise TypeError("benefits must be a string")
    job_data = {
        'company_name': company_name,
        'job_name': job_name,
        'location': location,
        'experience_level': experience_level,
        'required_skills': required_skills,
        'optional_skills': optional_skills,
        'salary': salary,
        'benefits': benefits,
        'description': description
    }
    
    job_ref = db.collection('jobs').add(job_data)
    return job_ref[1].id