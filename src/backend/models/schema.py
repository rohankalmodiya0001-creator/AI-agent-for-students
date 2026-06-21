from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class ResumeProfile(BaseModel):
    skills: List[str]
    projects: List[str]
    experience: str
    certifications: List[str]
    technologies: List[str]
    raw_text: str


class JobDescriptionProfile(BaseModel):
    required_skills: List[str]
    technologies: List[str]
    responsibilities: List[str]
    seniority_level: str
    keywords: List[str]
    raw_text: str


class SkillGapReport(BaseModel):
    missing_skills: List[str]
    weak_skills: List[str]
    strengths: List[str]
    match_score: float = Field(..., ge=0, le=100)
    readiness_score: float = Field(..., ge=0, le=100)
    summary: str


class InterviewQuestion(BaseModel):
    question: str
    topic: str
    difficulty: str
    follow_up: Optional[str] = None


class EvaluationMetrics(BaseModel):
    correctness: float = Field(..., ge=0, le=100)
    depth: float = Field(..., ge=0, le=100)
    communication: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=100)
    problem_solving: float = Field(..., ge=0, le=100)


class InterviewHistoryRecord(BaseModel):
    question: str
    topic: str
    answer: str
    evaluation: EvaluationMetrics
    feedback: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PerformanceTrend(BaseModel):
    technical_score: float = Field(..., ge=0, le=100)
    communication_score: float = Field(..., ge=0, le=100)
    problem_solving_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)
    readiness_score: float = Field(..., ge=0, le=100)
    weak_topics: List[str]
    strong_topics: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserSession(BaseModel):
    user_id: str
    session_id: str
    resume_profile: Optional[ResumeProfile]
    job_description_profile: Optional[JobDescriptionProfile]
    skill_gap_report: Optional[SkillGapReport]
    roadmap: Optional[List[str]]
    final_report: Optional[str]
    interview_history: Optional[List[InterviewHistoryRecord]]
    performance_trends: Optional[List[PerformanceTrend]]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentRequest(BaseModel):
    session_id: str
    payload: dict


class AgentResponse(BaseModel):
    agent_name: str
    output: dict
    status: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
