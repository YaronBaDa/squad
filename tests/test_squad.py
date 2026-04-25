"""Tests for Squad framework."""

import pytest
from squad.agents import AgentRole, LeadAgent, PlannerAgent, CoderAgent, ReviewerAgent
from squad.config import SquadConfig
from squad.orchestrator import SquadOrchestrator


class TestAgents:
    def test_lead_agent_creation(self):
        lead = LeadAgent()
        assert lead.role == AgentRole.LEAD

    def test_planner_agent_creation(self):
        planner = PlannerAgent()
        assert planner.role == AgentRole.PLANNER

    def test_coder_agent_creation(self):
        coder = CoderAgent()
        assert coder.role == AgentRole.CODER

    def test_reviewer_agent_creation(self):
        reviewer = ReviewerAgent()
        assert reviewer.role == AgentRole.REVIEWER

    def test_lead_routing(self):
        lead = LeadAgent()
        result = lead.receive_task("Add auth feature")
        assert result["routing"] == "planner"

    def test_planner_output(self):
        planner = PlannerAgent()
        result = planner.receive_task("Add auth feature")
        assert "design_doc" in result

    def test_coder_output(self):
        coder = CoderAgent()
        result = coder.receive_task("Add auth feature", {"design_doc": "auth plan"})
        assert "code_changes" in result

    def test_reviewer_output(self):
        reviewer = ReviewerAgent()
        result = reviewer.receive_task("Add auth feature", {"code_changes": "auth impl"})
        assert "approved" in result


class TestConfig:
    def test_default_config(self):
        config = SquadConfig()
        assert config.team["name"] == "default-squad"
        assert len(config.team["agents"]) == 4

    def test_config_validate(self):
        config = SquadConfig()
        issues = config.validate()
        assert len(issues) == 0


class TestOrchestrator:
    def test_run_task(self):
        config = SquadConfig()
        squad = SquadOrchestrator(config=config)
        result = squad.run("Add user authentication")
        assert result["task"] == "Add user authentication"
        assert len(result["steps"]) == 4  # lead, planner, coder, reviewer

    def test_status(self):
        config = SquadConfig()
        squad = SquadOrchestrator(config=config)
        squad.run("Test task")
        status = squad.status()
        assert status["tasks_completed"] == 1
        assert len(status["agents"]) == 4