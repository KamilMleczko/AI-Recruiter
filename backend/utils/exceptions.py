from typing import Dict, List, Any
class PDFSummarizerError(Exception):
    """Base exception for all PDFExtractor errors."""
    pass

class MissingFilePathError(PDFSummarizerError):
    """Raised when file_path field is missing from the input data."""
    def __init__(self):
        super().__init__("Missing 'file_path' in CV data.")

class SummarizerError(PDFSummarizerError):
    """Raised when text summarization of PDF fails."""
    def __init__(self, file_path: str, message: str = "Text summarization failed."):
        super().__init__(f"Failed to summarize text from '{file_path}': {message}")


class AnalyzerError(Exception):
    """Base exception for all PDFExtractor errors."""
    pass

class AnalyzerJSONParseError(AnalyzerError):
    """Raised when JSON parser failed in Analysis phase"""
    def __init__(self, text_to_be_parsed):
        super().__init__(f"Failed to parse json in Analysis phase. Text that failed parsing: {text_to_be_parsed}")

class JobMatcherError(Exception):
    """Raised when error is encountered in JobMatcher"""
    pass

class JobMatcherJSONLoadsError(JobMatcherError):
    """Raised when JSON loads function failed in Job Matching phase"""
    def __init__(self, text_to_be_parsed):
        super().__init__(f"Failed to parse json in Job Matching phase. Text that failed json.loads() : {text_to_be_parsed}")

class JobMatcherAnalysisNotFoundError(JobMatcherError):
    """Raised when JSON loads function failed in Job Matching phase"""
    def __init__(self):
        super().__init__("Analysis json not found")

class JobMatcherErrorSkillListEmpty(JobMatcherError):
    """Raised when candidate skill list is empty"""
    def __init__(self):
        super().__init__("Candidate skill list is empty. Error occured in Job Matcher.")

class JobMatcherInvalidWorkExp(JobMatcherError):
    """Raised when candidate work expierience couldn't be assesed"""
    def __init__(self, employment_history: List[Dict[str, Any]], e: Exception):
        super().__init__(f"Cv work expirience assesment failed with e: {e} and employment_history: {employment_history}")