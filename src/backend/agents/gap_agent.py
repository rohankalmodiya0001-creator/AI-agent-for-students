from ..models.schema import ResumeProfile, JobDescriptionProfile, SkillGapReport
from ..services.gap_service import SkillGapService


class SkillGapAgent:
    def __init__(self) -> None:
        self.service = SkillGapService()

    def analyze(self, resume: ResumeProfile, job_description: JobDescriptionProfile) -> SkillGapReport:
        return self.service.compare_profiles(resume, job_description)
