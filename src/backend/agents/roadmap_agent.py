from __future__ import annotations

from typing import List, Optional

from ..models.schema import PerformanceTrend, SkillGapReport
from ..services.roadmap_service import RoadmapService


class RoadmapAgent:
    def __init__(self) -> None:
        self.service = RoadmapService()

    def generate_roadmap(
        self,
        skill_gap: SkillGapReport,
        trends: Optional[PerformanceTrend] = None,
        interview_type: str | None = None,
    ) -> List[str]:
        return self.service.generate_roadmap(skill_gap, trends=trends, interview_type=interview_type)
