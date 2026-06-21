from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from backend.agents.interview_agent import InterviewAgent
from backend.models.schema import (
    EvaluationMetrics,
    InterviewHistoryRecord,
    InterviewQuestion,
    JobDescriptionProfile,
    PerformanceTrend,
    ResumeProfile,
    SkillGapReport,
)
from backend.services.evaluation_service import EvaluationService
from backend.services.gap_service import SkillGapService
from backend.services.jd_service import JobDescriptionService
from backend.services.memory_service import MemoryService
from backend.services.report_service import ReportService
from backend.services.roadmap_service import RoadmapService
from backend.services.resume_service import ResumeService
from backend.storage import memory_store
from backend.utils.text_processing import extract_entities_from_text


def test_resume_service_extracts_structured_profile() -> None:
    service = ResumeService()
    profile = service.parse_resume_text(
        "Senior Python engineer built RAG systems with Docker and MLOps. Certified AWS Practitioner."
    )

    assert "python" in profile.skills
    assert "docker" in profile.technologies
    assert "certified aws practitioner" in " ".join(profile.certifications)
    assert profile.raw_text.startswith("Senior Python")


def test_job_description_service_extracts_requirements() -> None:
    service = JobDescriptionService()
    profile = service.parse_job_description(
        "Senior role for a Python engineer. Experience with Docker, MLOps, and prompt engineering required."
    )

    assert "python" in profile.required_skills
    assert profile.seniority_level.lower() == "senior"
    assert "mlops" in profile.keywords


def test_gap_service_scores_profiles() -> None:
    resume = ResumeProfile(
        skills=["Python", "Docker"],
        projects=["RAG assistant"],
        experience="Built internal tooling",
        certifications=[],
        technologies=["Python"],
        raw_text="resume text",
    )
    jd = JobDescriptionProfile(
        required_skills=["Python", "MLOps"],
        technologies=["Docker", "Kubernetes"],
        responsibilities=["ship models"],
        seniority_level="Senior",
        keywords=["python"],
        raw_text="jd text",
    )

    report = SkillGapService().compare_profiles(resume, jd)

    assert report.match_score >= 0
    assert report.readiness_score >= 0
    assert "mlops" in report.missing_skills
    assert report.strengths


def test_evaluation_service_aggregates_history() -> None:
    history = [
        InterviewHistoryRecord(
            question="Q1",
            topic="rag",
            answer="A1",
            evaluation=EvaluationMetrics(
                correctness=80,
                depth=70,
                communication=60,
                confidence=75,
                problem_solving=85,
            ),
            feedback="good",
        ),
        InterviewHistoryRecord(
            question="Q2",
            topic="python",
            answer="A2",
            evaluation=EvaluationMetrics(
                correctness=60,
                depth=55,
                communication=65,
                confidence=50,
                problem_solving=60,
            ),
            feedback="improve",
        ),
    ]

    trend = EvaluationService().evaluate_history(history)

    assert trend.technical_score == pytest.approx(70.0)
    assert "python" in trend.weak_topics


def test_roadmap_service_prioritizes_weak_topics() -> None:
    skill_gap = SkillGapReport(
        missing_skills=["rag", "vector databases"],
        weak_skills=["prompt engineering"],
        strengths=["python"],
        match_score=60,
        readiness_score=50,
        summary="summary",
    )
    trend = PerformanceTrend(
        technical_score=65,
        communication_score=70,
        problem_solving_score=68,
        confidence_score=60,
        readiness_score=58,
        weak_topics=["rag"],
        strong_topics=["python"],
    )

    roadmap = RoadmapService().generate_roadmap(skill_gap, trends=trend, interview_type="RAG")

    assert any("rag" in step.lower() for step in roadmap)
    assert any("prompt engineering" in step.lower() for step in roadmap)


def test_interview_agent_handles_partial_answers() -> None:
    agent = InterviewAgent()
    questions = [
        InterviewQuestion(question="Explain RAG", topic="rag", difficulty="medium"),
        InterviewQuestion(question="Explain Python", topic="python", difficulty="medium"),
    ]

    history = agent.simulate_question_flow(questions, ["RAG uses retrieval and generation."])

    assert len(history) == 2
    assert history[1].answer == ""
    assert history[0].feedback


def test_report_service_generates_summary() -> None:
    report = ReportService().generate_report(
        SkillGapReport(
            missing_skills=["rag"],
            weak_skills=["prompt engineering"],
            strengths=["python"],
            match_score=70,
            readiness_score=55,
            summary="summary",
        ),
        PerformanceTrend(
            technical_score=72,
            communication_score=80,
            problem_solving_score=68,
            confidence_score=60,
            readiness_score=65,
            weak_topics=["rag"],
            strong_topics=["python"],
        ),
    )

    assert report.startswith("Final Interview Readiness Report")
    assert "rag" in report.lower()


def test_memory_service_round_trip(monkeypatch, tmp_path: Path) -> None:
    memory_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", memory_file)

    service = MemoryService()
    service.store_interview_record(
        "session-1",
        {
            "feedback": ["good"],
            "weak_topics": ["rag"],
            "strong_topics": ["python"],
            "adaptive_roadmap": ["study rag"],
            "question_count": 1,
        },
    )

    summary = service.build_progress_summary("session-1")

    assert summary["history_length"] == 1
    assert summary["adaptive_roadmap"] == ["study rag"]
    assert summary["weak_topics"] == ["rag"]
