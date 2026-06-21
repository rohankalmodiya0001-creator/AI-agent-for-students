from ..models.schema import ResumeProfile
from ..services.resume_service import ResumeService


class ResumeAnalysisAgent:
    def __init__(self) -> None:
        self.service = ResumeService()

    def analyze(self, file_path: str) -> ResumeProfile:
        return self.service.parse_resume(file_path)
