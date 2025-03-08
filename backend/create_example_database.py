import firebase_admin
from firebase_admin import firestore, credentials
from backend.database_handler import add_example_job_to_database, add_job_to_database
import os

# Initialize database and add example jobs, add your firebase key in "key.json" file before running

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
    experience_level="senior",
    years_of_experience=7,
    salary="$140,000 - $180,000",
    description="Looking for an experienced Frontend Developer with React expertise.",
    required_skills=["JavaScript", "React", "HTML", "CSS"],
    optional_skills=["TypeScript", "Next.js", "GraphQL", "Testing"],
    benefits="Competitive salary, equity package, medical insurance, 401(k), free meals, and fitness stipend."
)



jobs = [
    {
        "company_name": "Amazon",
        "job_name": "Software Engineer Intern",
        "location": "Seattle, WA",
        "experience_level": "intern",
        "years_of_experience": 0,
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
        "experience_level": "intern",
        "years_of_experience": 0,
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
        "experience_level": "junior",
        "years_of_experience": 2,
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
        "experience_level": "junior",
        "years_of_experience": 1,
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
        "experience_level": "mid",
        "years_of_experience": 3,
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
        "experience_level": "mid",
        "years_of_experience": 4,
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
        "experience_level": "senior",
        "years_of_experience": 6,
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
        "experience_level": "senior",
        "years_of_experience": 7,
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
        "experience_level": "mid",
        "years_of_experience": 4,
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
        "experience_level": "junior",
        "years_of_experience": 0,
        "salary": "$80,000 - $100,000",
        "description": "Junior System Administrator to support and maintain our IT infrastructure.",
        "required_skills": ["Linux", "Networking Basics", "Scripting (Bash/Python)"],
        "optional_skills": ["Cloud Platforms", "Automation Tools"],
        "benefits": "Employee volunteer program, health benefits, career growth opportunities."
    },

    {
    "company_name": "IBM",
    "job_name": "Senior Data Scientist",
    "location": "New York, NY",
    "experience_level": "senior",
    "years_of_experience": 6,
    "salary": "$170,000 - $220,000",
    "description": "Senior Data Scientist to develop and deploy advanced machine learning models.",
    "required_skills": ["Machine Learning", "Data Mining", "Python/R"],
    "optional_skills": ["Deep Learning", "Big Data Technologies"],
    "benefits": "Tuition reimbursement, health benefits, retirement plans."
  },

  {
    "company_name": "Adobe",
    "job_name": "Junior QA Engineer",
    "location": "San Jose, CA",
    "experience_level": "junior",
    "years_of_experience": 2,
    "salary": "$75,000 - $95,000",
    "description": "QA Engineer to develop and execute test cases for software applications.",
    "required_skills": ["Testing Methodologies", "Bug Tracking", "Scripting"],
    "optional_skills": ["Automation Testing", "Performance Testing"],
    "benefits": "Employee stock purchase plan, health benefits, flexible hours."
  },

  {
    "company_name": "Goldman Sachs",
    "job_name": "Junior Software Developer",
    "location": "New York, NY",
    "experience_level": "junior",
    "years_of_experience": 1,
    "salary": "$95,000 - $115,000",
    "description": "Junior developer to assist in building and maintaining financial software systems.",
    "required_skills": ["Java/C++", "Data Structures", "Problem Solving"],
    "optional_skills": ["Financial Domain Knowledge", "Cloud Services"],
    "benefits": "Competitive salary, health benefits, professional development."
  },
  {
    "company_name": "Tesco",
    "job_name": "Software Engineering Intern",
    "location": "Welwyn Garden City, UK",
    "experience_level": "intern",
    "years_of_experience": 0,
    "salary": "£2,000/month",
    "description": "Software engineering internship to contribute to retail technology projects.",
    "required_skills": ["Basic Programming", "Data Structures"],
    "optional_skills": ["Python", "Web Development"],
    "benefits": "Mentorship, practical experience, employee discounts."
  },
  {
    "company_name": "Boeing",
    "job_name": "Mid-Level Software Engineer",
    "location": "Seattle, WA",
    "experience_level": "mid",
    "years_of_experience": 4,
    "salary": "$125,000 - $155,000",
    "description": "Software engineer to develop and maintain aerospace software systems.",
    "required_skills": ["C++/Python", "Embedded Systems", "Software Testing"],
    "optional_skills": ["Aerospace Domain Knowledge", "Real-time Systems"],
    "benefits": "Comprehensive benefits, retirement plans, professional growth."
  },
  {
    "company_name": "Siemens",
    "job_name": "Senior Software Architect",
    "location": "Munich, Germany",
    "experience_level": "senior",
    "years_of_experience": 7,
    "salary": "€100,000 - €140,000",
    "description": "Software architect to design and lead industrial automation software projects.",
    "required_skills": ["System Design", "Leadership", "Industrial Automation"],
    "optional_skills": ["Cloud Technologies", "IoT"],
    "benefits": "Flexible work, health insurance, international opportunities."
  },
  {
    "company_name": "Walmart",
    "job_name": "Junior Data Engineer",
    "location": "Bentonville, AR",
    "experience_level": "junior",
    "years_of_experience": 2,
    "salary": "$80,000 - $100,000",
    "description": "Junior data engineer to build and maintain data pipelines for retail analytics.",
    "required_skills": ["SQL", "ETL Processes", "Data Warehousing"],
    "optional_skills": ["Python", "Cloud Data Platforms"],
    "benefits": "Employee discounts, health benefits, career development."
  },
  {
    "company_name": "Ford",
    "job_name": "Mid-Level Embedded Software Engineer",
    "location": "Dearborn, MI",
    "experience_level": "mid",
    "years_of_experience": 3,
    "salary": "$110,000 - $140,000",
    "description": "Embedded software engineer to develop software for automotive systems.",
    "required_skills": ["C/C++", "Embedded Systems", "Real-time Operating Systems"],
    "optional_skills": ["Automotive Standards", "CAN/LIN Protocols"],
    "benefits": "Retirement plans, health insurance, employee vehicle discounts."
  },
  {
    "company_name": "HSBC",
    "job_name": "Senior Cybersecurity Engineer",
    "location": "London, UK",
    "experience_level": "senior",
    "years_of_experience": 6,
    "salary": "£80,000 - £120,000",
    "description": "Cybersecurity engineer to protect financial systems from threats.",
    "required_skills": ["Network Security", "Incident Response", "Security Audits"],
    "optional_skills": ["Cloud Security", "Penetration Testing"],
    "benefits": "Pension plans, health benefits, global career opportunities."
  },
  {
    "company_name": "John Deere",
    "job_name": "Junior Software Test Engineer",
    "location": "Moline, IL",
    "experience_level": "junior",
    "years_of_experience": 1,
    "salary": "$70,000 - $90,000",
    "description": "Software test engineer to ensure quality of agricultural technology software.",
    "required_skills": ["Software Testing", "Bug Tracking", "Scripting"],
    "optional_skills": ["Automation Testing", "Agile Methodologies"],
    "benefits": "Competitive salary, health benefits, retirement plans."
  },
    {
    "company_name": "FedEx",
    "job_name": "Mid-Level DevOps Engineer",
    "location": "Memphis, TN",
    "experience_level": "mid",
    "years_of_experience": 5,
    "salary": "$115,000 - $145,000",
    "description": "DevOps engineer to automate deployment and maintain logistics infrastructure.",
    "required_skills": ["Docker/Kubernetes", "CI/CD", "Cloud Platforms"],
    "optional_skills": ["Terraform", "Ansible"],
    "benefits": "Health benefits, retirement plans, employee discounts."
  },
  {
    "company_name": "Nestle",
    "job_name": "Senior Data Scientist",
    "location": "Vevey, Switzerland",
    "experience_level": "senior",
    "years_of_experience": 8,
    "salary": "CHF 120,000 - CHF 180,000",
    "description": "Data Scientist to develop and deploy advanced machine learning models for consumer analytics.",
    "required_skills": ["Machine Learning", "Data Mining", "Python/R"],
    "optional_skills": ["Deep Learning", "Big Data Technologies"],
    "benefits": "Pension plans, health benefits, international career paths."
  }

]

for job in jobs:
    add_job_to_database(db, **job)