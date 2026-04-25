"""
Squad — AI Dev Team Framework
Multi-agent orchestration for collaborative software development.
"""

__version__ = "0.1.0"

from squad.agents import Agent, PlannerAgent, CoderAgent, ReviewerAgent, LeadAgent
from squad.orchestrator import SquadOrchestrator
from squad.config import SquadConfig

__all__ = [
    "Agent",
    "PlannerAgent", 
    "CoderAgent",
    "ReviewerAgent", 
    "LeadAgent",
    "SquadOrchestrator",
    "SquadConfig",
]