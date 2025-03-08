# app.py (using Flask for simplicity)
from flask import Flask, request, jsonify
import tempfile
import os
import asyncio
from process_cv import start_process

app = Flask(__name__)

@app.route('/api/process-cv', methods=['POST'])
def process_cv():
    if 'cv_file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['cv_file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400
    
    # Save the uploaded file to a temporary location
    temp_dir = tempfile.gettempdir()
    temp_filepath = os.path.join(temp_dir, file.filename)
    file.save(temp_filepath)
    
    try:
        # Run the processing function
        ctx = asyncio.run(process_cv(temp_filepath))
        # Example structure of the response
        
        

        summarization_markdown = ctx["summarizer_output"]["structured_text"]
        analysis_json = ctx["analysis_results"]["analysis_json"]
        jobs_matched_json = [convert_to_markdown(ctx["job_matches"]["matched_jobs"][num], num) for num in range(3)]
        evaluation_markdown = [ctx["candidate_to_jobs_evaluation"][num]["evaluator_report"] for num in range(3)]
        

        # Return the response
        result = {
            "status": "success",
            "summarization": summarization_markdown,
            "analysis": "",
            "jobs_matched": jobs_matched_json,
            "evaluation": evaluation_markdown
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

async def process_cv(file_path):
    cv_data = {
        "file_path": file_path
    }
    
    ctx = await start_process(cv_data)
    count = 0
    
    while ctx["status"] == "no_jobs_matched" and count < 3:
        count += 1
        ctx = await start_process(cv_data)
    
    return ctx

def convert_to_markdown(data, num):
    markdown = f"""
## {data['job_name']} at {data['company_name']}
- **Location:** {data['location']} 
- **Salary:** {data['salary']} 

Job Description: {data['description']} \n
Experience Level: **{data['experience_level'].capitalize()}** \n
Years of Experience Required: **{data['years_of_experience']} years** \n

### Required Skills
"""
    for skill in data['required_skills']:
        markdown += f"- {skill}\n"
    
    markdown += "\n### Optional Skills\n"
    for skill in data['optional_skills']:
        markdown += f"- {skill}\n"
    
    markdown += f"""
\n Benefits: {data['benefits']}
### Candidate Skill Scores
- **Required Skills Score:** {data['required_skills_score']}%
- **Optional Skills Score:** {data['optional_skills_score']}%
"""
    
    return markdown

if __name__ == "__main__":
    app.run(debug=True)