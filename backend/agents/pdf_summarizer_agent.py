#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime as dt
from pdfminer.high_level import extract_text
from utils.exceptions import SummarizerError, MissingFilePathError
class PdfSummarizerAgent(BaseAgent):
    def __init__(self):
        """Leverages llm to Abstractively summarize the pdf"""
        super().__init__(
            name = "PdfSummarizer Agent",
            instructions = """ Extract and structure information from resume(cv), that will be given to you as input from the user.
            Split the text into following sections:
            -Personal Information
            -Work Expierience (list ALL companies and roles candidate held with time periods, including internships)
            -Candidate expierience level (intern/junior/mid/senior/not_stated) 
                For Candidate experience level list intern/junior/mid/senior ONLY IF IT WAS EXPLICITLY STATED in cv, if it was not then list ONLY "Not Stated" under that category.
                If there were EXPLICIT mentions of DIFFRENT expierience levels across the jobs then list ONLY the highest expierience level (example: first job: Junior, second Job: Mid, you list ONLY Mid).
            -Education
            -Skills 
            -Key Achievements
            -Main Areas of Expertise

            Provide your answer in clear and structured format. 
            Do not shorten the resume too much, keep it as close to the original as possible, just in more concise manner.
            """
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        print("⌛ Processing pdf file: ")
        cv_data = eval(messages[-1]["content"])

        if not cv_data.get("file_path"):
            raise MissingFilePathError()

        file_path = cv_data["file_path"]
        try:
            unstructured_text = extract_text(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except Exception as e:
            raise SummarizerError(file_path, str(e))

        res = self.query_ollama(unstructured_text)
        #print(res)
        return {
            "unstructured_text": unstructured_text,
            "structured_text": res,
            "timestamp": dt.datetime.now().strftime("%H:%M %d-%m-%Y")
        }