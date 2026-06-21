try:
    from langgraph import Graph, Node
except Exception:
    # Provide lightweight fallback for environments where langgraph API differs or is unavailable.
    class Node:
        def __init__(self, name, func):
            self.name = name
            self.func = func

    class Graph:
        def __init__(self):
            self.nodes = {}
            self.edges = {}

        def add_nodes(self, *nodes):
            for n in nodes:
                self.nodes[n.name] = n

        def add_edge(self, src, dst):
            self.edges.setdefault(src, []).append(dst)

from ..agents.resume_agent import ResumeAnalysisAgent
from ..agents.jd_agent import JobDescriptionAgent
from ..agents.gap_agent import SkillGapAgent
from ..agents.research_agent import ResearchAgent
from ..agents.roadmap_agent import RoadmapAgent
from ..agents.interview_agent import InterviewAgent
from ..agents.evaluation_agent import EvaluationAgent
from ..agents.report_agent import ReportAgent
from ..models.schema import (
    InterviewQuestion,
    JobDescriptionProfile,
    ResumeProfile,
    SkillGapReport,
    PerformanceTrend,
)


class LangGraphWorkflow:
    def __init__(self) -> None:
        self.graph = Graph()
        self.resume_agent = ResumeAnalysisAgent()
        self.jd_agent = JobDescriptionAgent()
        self.gap_agent = SkillGapAgent()
        self.research_agent = ResearchAgent()
        self.roadmap_agent = RoadmapAgent()
        self.interview_agent = InterviewAgent()
        self.evaluation_agent = EvaluationAgent()
        self.report_agent = ReportAgent()

    def build(self) -> Graph:
        resume_node = Node("resume_analysis", self.resume_analysis)
        jd_node = Node("jd_analysis", self.job_description_analysis)
        gap_node = Node("skill_gap_analysis", self.skill_gap_analysis)
        research_node = Node("research_retrieval", self.research_retrieval)
        roadmap_node = Node("roadmap_generation", self.roadmap_generation)
        interview_node = Node("mock_interview", self.mock_interview)
        evaluation_node = Node("evaluation", self.evaluate)
        report_node = Node("final_report", self.final_report)

        self.graph.add_nodes(resume_node, jd_node, gap_node, research_node, roadmap_node, interview_node, evaluation_node, report_node)
        self.graph.add_edge("resume_analysis", "skill_gap_analysis")
        self.graph.add_edge("jd_analysis", "skill_gap_analysis")
        self.graph.add_edge("skill_gap_analysis", "research_retrieval")
        self.graph.add_edge("research_retrieval", "roadmap_generation")
        self.graph.add_edge("roadmap_generation", "mock_interview")
        self.graph.add_edge("mock_interview", "evaluation")
        self.graph.add_edge("evaluation", "final_report")

        return self.graph

    def resume_analysis(self, input_data: dict) -> dict:
        resume_profile = self.resume_agent.analyze(input_data["resume_path"])
        return {"resume_profile": resume_profile.model_dump()}

    def job_description_analysis(self, input_data: dict) -> dict:
        jd_profile = self.jd_agent.analyze(input_data["job_description_text"])
        return {"job_description_profile": jd_profile.model_dump()}

    def skill_gap_analysis(self, input_data: dict) -> dict:
        resume_profile = ResumeProfile(**input_data["resume_profile"])
        jd_profile = JobDescriptionProfile(**input_data["job_description_profile"])
        report = self.gap_agent.analyze(resume_profile, jd_profile)
        return {"skill_gap_report": report.model_dump()}

    def research_retrieval(self, input_data: dict) -> dict:
        query = input_data["query"]
        topics = input_data.get("topics", [])
        context = self.research_agent.retrieve_learning_context(query, topics)
        return {"research_context": context}

    def roadmap_generation(self, input_data: dict) -> dict:
        skill_gap_report = SkillGapReport(**input_data["skill_gap_report"])
        trends_payload = input_data.get("performance_trends")
        trends = PerformanceTrend(**trends_payload) if trends_payload else None
        roadmap = self.roadmap_agent.generate_roadmap(
            skill_gap_report,
            trends=trends,
            interview_type=input_data.get("interview_type"),
        )
        return {"roadmap": roadmap}

    def mock_interview(self, input_data: dict) -> dict:
        skill_gap_report = SkillGapReport(**input_data["skill_gap_report"])
        questions = self.interview_agent.prepare_questions(
            skill_gap_report,
            input_data.get("interview_type", "machine learning"),
        )
        return {"questions": [question.model_dump() for question in questions]}

    def evaluate(self, input_data: dict) -> dict:
        questions = [InterviewQuestion(**question) for question in input_data["questions"]]
        answers = input_data.get("answers", [])
        history = self.interview_agent.simulate_question_flow(questions, answers)
        trends = self.evaluation_agent.evaluate(history)
        adaptive_roadmap = self.roadmap_agent.generate_roadmap(
            SkillGapReport(**input_data["skill_gap_report"]),
            trends=trends,
            interview_type=input_data.get("interview_type"),
        )
        return {
            "interview_history": [record.model_dump() for record in history],
            "performance_trends": trends.model_dump(),
            "adaptive_roadmap": adaptive_roadmap,
        }

    def final_report(self, input_data: dict) -> dict:
        skill_gap_report = SkillGapReport(**input_data["skill_gap_report"])
        trends = PerformanceTrend(**input_data["performance_trends"])
        final_report = self.report_agent.generate_report(skill_gap_report, trends)
        return {"final_report": final_report}
