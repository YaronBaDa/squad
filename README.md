# Squad — AI Dev Team Framework

**Multi-agent orchestration for collaborative software development.**

Squad coordinates AI agents (Planner, Coder, Reviewer, Lead) into a structured workflow — plan → implement → review → approve. Each agent has a clear role and hands off to the next.

## Install

```bash
pip install -e .
```

## Quick Start

```python
from squad import SquadOrchestrator, SquadConfig

config = SquadConfig()
squad = SquadOrchestrator(config=config)

result = squad.run("Add user authentication")
print(result)
```

## CLI

```bash
squad run "Add login page"
squad status
squad init
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **Lead** | Routes tasks, approves output | Flagship |
| **Planner** | Specs & design docs | Reasoning |
| **Coder** | Implementation | Coding |
| **Reviewer** | Quality gates & security | Analysis |

## Config

See `squad.config.yml` for team and workflow configuration.

## License

MIT