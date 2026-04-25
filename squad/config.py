"""Squad Configuration — loads and validates squad.config.yml."""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None


DEFAULT_CONFIG = {
    "team": {
        "name": "default-squad",
        "agents": [
            {"role": "lead", "model": "flagship", "description": "Orchestrates tasks, routes work, approves final output"},
            {"role": "planner", "model": "reasoning", "description": "Writes specs, architecture decisions, design docs"},
            {"role": "coder", "model": "coding", "description": "Implements features, fixes bugs, refactors code"},
            {"role": "reviewer", "model": "analysis", "description": "Code review, security audit, quality gates"},
        ],
    },
    "workflow": [
        {"name": "plan", "agent": "planner", "output": "design_doc"},
        {"name": "implement", "agent": "coder", "input": "design_doc", "output": "code_changes"},
        {"name": "review", "agent": "reviewer", "input": "code_changes", "output": "review_feedback"},
        {"name": "approve", "agent": "lead", "input": "review_feedback", "output": "approved_changes"},
    ],
    "defaults": {
        "auto_push": True,
        "test_before_merge": True,
        "require_review": True,
    },
}


@dataclass
class SquadConfig:
    """Configuration for a Squad team."""
    team: Dict[str, Any] = field(default_factory=lambda: DEFAULT_CONFIG["team"])
    workflow: List[Dict[str, Any]] = field(default_factory=lambda: DEFAULT_CONFIG["workflow"])
    defaults: Dict[str, Any] = field(default_factory=lambda: DEFAULT_CONFIG["defaults"])

    @classmethod
    def from_file(cls, path: str = "squad.config.yml") -> "SquadConfig":
        """Load config from YAML file."""
        if not os.path.exists(path):
            return cls()

        if yaml is None:
            raise ImportError("PyYAML required: pip install pyyaml")

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(
            team=data.get("team", DEFAULT_CONFIG["team"]),
            workflow=data.get("workflow", DEFAULT_CONFIG["workflow"]),
            defaults=data.get("defaults", DEFAULT_CONFIG["defaults"]),
        )

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        valid_roles = {"lead", "planner", "coder", "reviewer"}
        
        for agent in self.team.get("agents", []):
            if agent.get("role") not in valid_roles:
                issues.append(f"Invalid agent role: {agent.get('role')}")
        
        if not self.workflow:
            issues.append("No workflow steps defined")
            
        return issues