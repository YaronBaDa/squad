"""Base Agent and role-specific implementations."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AgentRole(Enum):
    LEAD = "lead"
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"


@dataclass
class Agent:
    """Base agent in the squad."""
    role: AgentRole
    model: str = "flagship"
    description: str = ""
    context: list = field(default_factory=list)

    def receive_task(self, task: str, input_artifacts: dict = None) -> dict:
        """Receive a task and any input from previous agent."""
        self.context.append({"task": task, "input": input_artifacts or {}})
        return self.execute(task, input_artifacts)

    def execute(self, task: str, input_artifacts: dict = None) -> dict:
        """Execute the task. Override in subclasses."""
        raise NotImplementedError

    def handoff(self, output: dict) -> dict:
        """Package output for the next agent."""
        return {
            "agent": self.role.value,
            "output": output,
        }


@dataclass
class LeadAgent(Agent):
    """Orchestrates the squad, routes tasks, approves final output."""
    role: AgentRole = field(default=AgentRole.LEAD)
    model: str = "flagship"

    def execute(self, task: str, input_artifacts: dict = None) -> dict:
        # Lead decides which agent to route to
        return {"routing": "planner", "task": task}


@dataclass  
class PlannerAgent(Agent):
    """Creates specs, architecture decisions, and design docs."""
    role: AgentRole = field(default=AgentRole.PLANNER)
    model: str = "reasoning"

    def execute(self, task: str, input_artifacts: dict = None) -> dict:
        return {
            "design_doc": f"Plan for: {task}",
            "specifications": [],
            "architecture_decisions": [],
        }


@dataclass
class CoderAgent(Agent):
    """Implements features, fixes bugs, and refactors code."""
    role: AgentRole = field(default=AgentRole.CODER)
    model: str = "coding"

    def execute(self, task: str, input_artifacts: dict = None) -> dict:
        design = input_artifacts.get("design_doc", "") if input_artifacts else ""
        return {
            "code_changes": f"Implementation of: {task}",
            "design_based_on": design,
        }


@dataclass
class ReviewerAgent(Agent):
    """Code review, security audit, and quality gates."""
    role: AgentRole = field(default=AgentRole.REVIEWER)
    model: str = "analysis"

    def execute(self, task: str, input_artifacts: dict = None) -> dict:
        code = input_artifacts.get("code_changes", "") if input_artifacts else ""
        return {
            "review_feedback": f"Review of: {task}",
            "approved": True,
            "comments": [],
        }