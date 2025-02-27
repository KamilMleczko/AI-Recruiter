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