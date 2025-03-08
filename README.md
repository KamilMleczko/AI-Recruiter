# AI-Recruiter
Leverages LLM Swarm to process cv and check if candidate is fit for any of the jobs in a database. 
Then chooses best fits and generates reports and evaluations.

## Install Requirements:
### Python version: 3.12.9
### Option1: Installation using Conda:
```bash
conda env create -f job-recruiter.yml
conda activate [env_name]
```
### Option2: Installation using python venv:
* For Linux/Mac
```bash
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
* For Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## How to Run
In first terminal:
```bash
cd frontend
npm install
npm run dev
```

In second terminal:
```bash
cd backend
flask run
```
