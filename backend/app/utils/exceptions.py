from fastapi import HTTPException

class VideoSummarizerException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)

class InvalidURLError(VideoSummarizerException):
    def __init__(self, detail: str = "Invalid URL provided"):
        super().__init__(detail=detail, status_code=400)

class TranscriptionError(VideoSummarizerException):
    def __init__(self, detail: str = "Error during transcription", status_code: int = 500):
        super().__init__(detail=detail, status_code=status_code)

class AIServiceError(VideoSummarizerException):
    def __init__(self, detail: str = "Error interacting with AI service"):
        super().__init__(detail=detail, status_code=502)

class FileProcessingError(VideoSummarizerException):
    def __init__(self, detail: str = "Error processing file"):
        super().__init__(detail=detail, status_code=500)

class QuotaExceededError(VideoSummarizerException):
    def __init__(self, detail: str = "Quota exceeded"):
        super().__init__(detail=detail, status_code=429)

class UnsupportedFormatError(VideoSummarizerException):
    def __init__(self, detail: str = "Unsupported format"):
        super().__init__(detail=detail, status_code=415)
