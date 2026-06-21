from ..models.schema import PerformanceTrend, SkillGapReport
from ..services.report_service import ReportService


class ReportAgent:
    def __init__(self) -> None:
        self.service = ReportService()

    def generate_report(self, skill_gap: SkillGapReport, trends: PerformanceTrend) -> str:
        return self.service.generate_report(skill_gap, trends)
