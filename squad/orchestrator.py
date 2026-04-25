"""Squad Orchestrator — manages workflow and agent handoffs."""

from dataclasses import dataclass, field
from typing import List, Optional
from .agents import Agent, AgentRole, LeadAgent, PlannerAgent, CoderAgent, ReviewerAgent
from .config import SquadConfig


@dataclass
class SquadOrchestrator:
    """Routes tasks through the squad workflow."""
    config: SquadConfig = None
    agents: dict = field(default_factory=dict)
    history: list = field(default_factory=list)

    def __post_init__(self):
        if self.config is None:
            self.config = SquadConfig()
        
        # Initialize agents from config
        role_map = {
            AgentRole.LEAD: LeadAgent,
            AgentRole.PLANNER: PlannerAgent,
            AgentRole.CODER: CoderAgent,
            AgentRole.REVIEWER: ReviewerAgent,
        }
        for agent_cfg in self.config.team.get("agents", []):
            role = AgentRole(agent_cfg["role"])
            agent_cls = role_map[role]
            self.agents[role] = agent_cls(
                role=role,
                model=agent_cfg.get("model", "flagship"),
                description=agent_cfg.get("description", ""),
            )

    def run(self, task: str) -> dict:
        """Run a task through the full squad workflow."""
        result = {"task": task, "steps": []}
        
        # Step 1: Lead routes
        lead = self.agents.get(AgentRole.LEAD)
        if lead:
            routing = lead.receive_task(task)
            result["steps"].append({"agent": "lead", "output": routing})

        # Step 2: Planner creates design
        planner = self.agents.get(AgentRole.PLANNER)
        if planner:
            plan = planner.receive_task(task)
            result["steps"].append({"agent": "planner", "output": plan})

        # Step 3: Coder implements
        coder = self.agents.get(AgentRole.CODER)
        if coder:
            plan_output = result["steps"][-1]["output"] if result["steps"] else {}
            code = coder.receive_task(task, plan_output)
            result["steps"].append({"agent": "coder", "output": code})

        # Step 4: Reviewer checks
        reviewer = self.agents.get(AgentRole.REVIEWER)
        if reviewer:
            code_output = result["steps"][-1]["output"] if result["steps"] else {}
            review = reviewer.receive_task(task, code_output)
            result["steps"].append({"agent": "reviewer", "output": review})

        self.history.append(result)
        return result

    def status(self) -> dict:
        """Get current squad status."""
        return {
            "agents": {r.value: a.description for r, a in self.agents.items()},
            "tasks_completed": len(self.history),
            "last_task": self.history[-1]["task"] if self.history else None,
        }