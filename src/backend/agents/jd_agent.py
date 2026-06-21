from ..models.schema import JobDescriptionProfile
from ..services.jd_service import JobDescriptionService


class JobDescriptionAgent:
    def __init__(self) -> None:
        self.service = JobDescriptionService()

    def analyze(self, text: str) -> JobDescriptionProfile:
        return self.service.parse_job_description(text)
