# AI-Recruiter
Leverages LLM Swarm to process cv and check if candidate is fit for any of the jobs in a database. 
Then chooses best fits and generates reports and evaluations.

![image alt](https://github.com/KamilMleczko/AI-Recruiter/blob/0f6bc27cd131e719045c580a0b63cad581c15ef7/sc1.png?raw=true)

![image alt](https://github.com/KamilMleczko/AI-Recruiter/blob/8b458fe018844fa239bd5ae392c922341168e2c5/sc3.png?raw=true)

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
