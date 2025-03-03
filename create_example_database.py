import firebase_admin
from firebase_admin import firestore, credentials
from database_handler import add_example_job_to_database, add_job_to_database

cred = credentials.Certificate('key.json')
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
print(f"Added new job with ID: {new_job_id}")