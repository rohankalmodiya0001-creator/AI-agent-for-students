from typing import List, Optional

from pydantic import BaseModel, Field


class ResumeUploadRequest(BaseModel):
    resume_path: str


class JobDescriptionUploadRequest(BaseModel):
    job_description_text: str


class SkillGapAnalysisRequest(BaseModel):
    resume_profile: dict
    job_description_profile: dict


class ResearchRequest(BaseModel):
    query: str
    topics: Optional[List[str]] = None


class RoadmapRequest(BaseModel):
    skill_gap_report: dict
    performance_trends: Optional[dict] = None
    interview_type: Optional[str] = None


class MockInterviewRequest(BaseModel):
    skill_gap_report: dict
    interview_type: str


class InterviewEvaluationRequest(BaseModel):
    session_id: str = Field(default="default")
    questions: List[dict]
    answers: List[str]


class FinalReportRequest(BaseModel):
    session_id: str = Field(default="default")
    skill_gap_report: dict
    performance_trends: dict
