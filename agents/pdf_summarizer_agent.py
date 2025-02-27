#GIT
from .base_agent import BaseAgent
from typing import Dict, Any
import datetime
from pdfminer.high_level import extract_text
from utils.exceptions import SummarizerError, MissingFilePathError
class PdfSummarizerAgent(BaseAgent):
    def __init__(self):
        """Leverages llm to Abstractively summarize the pdf"""
        super().__init__(
            name = "PdfSummarizer Agent",
            instructions = """ Extract and structure information from resume(cv),
            Focus on:
            -Personal Information
            -Work Expierience
            -Education
            -Skills and Qualifications

            Provide your answer in clear and structured format.
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

        return {
            "unstructured_text": unstructured_text,
            "structured_text": res,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
        }