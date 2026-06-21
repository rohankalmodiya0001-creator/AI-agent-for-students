from fastapi import APIRouter, HTTPException

from ..agents.langgraph_workflow import LangGraphWorkflow
from ..services.ingestion_service import IngestionService
from ..services.memory_service import MemoryService
from .schemas import (
    FinalReportRequest,
    InterviewEvaluationRequest,
    JobDescriptionUploadRequest,
    MockInterviewRequest,
    ResearchRequest,
    ResumeUploadRequest,
    RoadmapRequest,
    SkillGapAnalysisRequest,
)

router = APIRouter()
_workflow: LangGraphWorkflow | None = None
memory_service = MemoryService()
_ingestion_service: IngestionService | None = None


def get_ingestion_service() -> IngestionService:
    global _ingestion_service
    if _ingestion_service is None:
        _ingestion_service = IngestionService()
    return _ingestion_service


def get_workflow() -> LangGraphWorkflow:
    global _workflow
    if _workflow is None:
        _workflow = LangGraphWorkflow()
    return _workflow


@router.post("/resume")
def upload_resume(request: ResumeUploadRequest):
    try:
        return get_workflow().resume_analysis(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/job-description")
def upload_job_description(request: JobDescriptionUploadRequest):
    try:
        return get_workflow().job_description_analysis(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/skill-gap")
def skill_gap_analysis(request: SkillGapAnalysisRequest):
    try:
        return get_workflow().skill_gap_analysis(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/research")
def research(request: ResearchRequest):
    try:
        return get_workflow().research_retrieval(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/roadmap")
def roadmap(request: RoadmapRequest):
    try:
        return get_workflow().roadmap_generation(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/ingest")
def ingest_knowledge_base():
    try:
        return get_ingestion_service().ingest_knowledge_base()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/ingest/documents")
def list_knowledge_documents():
    try:
        return get_ingestion_service().list_documents()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/mock-interview")
def mock_interview(request: MockInterviewRequest):
    try:
        return get_workflow().mock_interview(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/evaluate")
def evaluate(request: InterviewEvaluationRequest):
    try:
        result = get_workflow().evaluate(request.model_dump())
        session_id = request.session_id
        session_record = {
            "question_count": len(request.questions),
            "weak_topics": result.get("performance_trends", {}).get("weak_topics", []),
            "strong_topics": result.get("performance_trends", {}).get("strong_topics", []),
            "feedback": [item.get("feedback") for item in result["interview_history"]],
            "adaptive_roadmap": result.get("adaptive_roadmap", []),
        }
        memory_service.store_interview_record(session_id, session_record)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/final-report")
def final_report(request: FinalReportRequest):
    try:
        return get_workflow().final_report(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/session/{session_id}/memory")
def session_memory(session_id: str):
    try:
        return memory_service.build_progress_summary(session_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
