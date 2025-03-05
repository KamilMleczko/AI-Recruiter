import firebase_admin
from firebase_admin import firestore, credentials
from database_handler import add_example_job_to_database, add_job_to_database
import os

path = os.path.join('.', 'key.json')
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()

add_example_job_to_database(db)

new_job_id = add_job_to_database(
    db,
    company_name="Google",
    job_name="Frontend Developer",
    location="Remote",
    experience_level="Senior",
    salary="$140,000 - $180,000",
    description="Looking for an experienced Frontend Developer with React expertise.",
    required_skills=["JavaScript", "React", "HTML", "CSS"],
    optional_skills=["TypeScript", "Next.js", "GraphQL", "Testing"],
    benefits="Competitive salary, equity package, medical insurance, 401(k), free meals, and fitness stipend."
)


# 10 more jobs
jobs = [
    {
        "company_name": "Amazon",
        "job_name": "Software Engineer Intern",
        "location": "Seattle, WA",
        "experience_level": "Intern",
        "salary": "$30 - $40/hour",
        "description": "Seeking a motivated Software Engineer Intern to contribute to our team.",
        "required_skills": ["Python", "Java", "Basic Algorithm Knowledge"],
        "optional_skills": ["AWS", "Data Structures"],
        "benefits": "Paid internship, mentorship, potential for full-time offer."
    },
    {
        "company_name": "Microsoft",
        "job_name": "Data Analyst Intern",
        "location": "Redmond, WA",
        "experience_level": "Intern",
        "salary": "$25 - $35/hour",
        "description": "Data Analyst Intern to support data-driven decision making.",
        "required_skills": ["SQL", "Excel", "Data Visualization"],
        "optional_skills": ["Python", "R"],
        "benefits": "Paid internship, networking opportunities, learning from experts."
    },
    {
        "company_name": "Meta",
        "job_name": "Junior Backend Developer",
        "location": "Menlo Park, CA",
        "experience_level": "Junior",
        "salary": "$90,000 - $110,000",
        "description": "Junior Backend Developer to build scalable systems.",
        "required_skills": ["Python", "Django/Flask", "Database Knowledge"],
        "optional_skills": ["Docker", "Kubernetes", "Cloud Platforms"],
        "benefits": "Competitive salary, health insurance, learning and development opportunities."
    },
    {
        "company_name": "Apple",
        "job_name": "Junior iOS Developer",
        "location": "Cupertino, CA",
        "experience_level": "Junior",
        "salary": "$85,000 - $105,000",
        "description": "Join our team as a Junior iOS Developer and contribute to innovative apps.",
        "required_skills": ["Swift", "iOS SDK", "Xcode"],
        "optional_skills": ["Objective-C", "UI/UX Design"],
        "benefits": "Employee discounts, health benefits, collaborative environment."
    },
    {
        "company_name": "Netflix",
        "job_name": "Mid-Level DevOps Engineer",
        "location": "Los Gatos, CA",
        "experience_level": "Mid",
        "salary": "$120,000 - $150,000",
        "description": "Mid-Level DevOps Engineer to automate and improve our infrastructure.",
        "required_skills": ["AWS", "Terraform", "CI/CD"],
        "optional_skills": ["Kubernetes", "Ansible", "Monitoring Tools"],
        "benefits": "Unlimited vacation, competitive pay, stock options, excellent healthcare."
    },
    {
        "company_name": "Spotify",
        "job_name": "Mid-Level Data Scientist",
        "location": "New York, NY",
        "experience_level": "Mid",
        "salary": "$115,000 - $145,000",
        "description": "Data Scientist to analyze user behavior and improve our platform.",
        "required_skills": ["Python", "Machine Learning", "Statistical Analysis"],
        "optional_skills": ["Big Data Tools", "A/B Testing"],
        "benefits": "Flexible work hours, music streaming subscription, health and wellness programs."
    },
    {
        "company_name": "Tesla",
        "job_name": "Senior Embedded Software Engineer",
        "location": "Austin, TX",
        "experience_level": "Senior",
        "salary": "$150,000 - $190,000",
        "description": "Senior Embedded Software Engineer to develop cutting-edge automotive systems.",
        "required_skills": ["C/C++", "Embedded Systems", "Real-Time Operating Systems"],
        "optional_skills": ["Automotive Protocols", "Hardware Debugging"],
        "benefits": "Stock options, competitive salary, innovative projects, health benefits."
    },
        {
        "company_name": "Adobe",
        "job_name": "Senior UX/UI Designer",
        "location": "San Jose, CA",
        "experience_level": "Senior",
        "salary": "$145,000 - $185,000",
        "description": "Lead design projects as a Senior UX/UI Designer.",
        "required_skills": ["Figma", "Adobe XD", "User Research"],
        "optional_skills": ["Prototyping", "Motion Design"],
        "benefits": "Creative environment, professional development, excellent health insurance."
    },
    {
        "company_name": "Intel",
        "job_name": "Mid-Level Hardware Engineer",
        "location": "Santa Clara, CA",
        "experience_level": "Mid",
        "salary": "$125,000 - $155,000",
        "description": "Mid-Level Hardware Engineer to design and test new hardware components.",
        "required_skills": ["Verilog/VHDL", "Digital Design", "Circuit Analysis"],
        "optional_skills": ["FPGA", "PCB Design"],
        "benefits": "Competitive salary, tuition reimbursement, employee stock purchase plan."
    },
    {
        "company_name": "Salesforce",
        "job_name": "Junior System Administrator",
        "location": "San Francisco, CA",
        "experience_level": "Junior",
        "salary": "$80,000 - $100,000",
        "description": "Junior System Administrator to support and maintain our IT infrastructure.",
        "required_skills": ["Linux", "Networking Basics", "Scripting (Bash/Python)"],
        "optional_skills": ["Cloud Platforms", "Automation Tools"],
        "benefits": "Employee volunteer program, health benefits, career growth opportunities."
    }
]

for job in jobs:
    add_job_to_database(db, **job)