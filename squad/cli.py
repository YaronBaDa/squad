"""Squad CLI — command-line interface for the Squad framework."""

import argparse
import json
import sys
from .config import SquadConfig
from .orchestrator import SquadOrchestrator


def main():
    parser = argparse.ArgumentParser(description="Squad — AI Dev Team Framework")
    subparsers = parser.add_subparsers(dest="command", help="Squad commands")

    # run command
    run_parser = subparsers.add_parser("run", help="Run a task through the squad")
    run_parser.add_argument("task", help="The task description")
    run_parser.add_argument("--config", default="squad.config.yml", help="Config file path")

    # status command
    status_parser = subparsers.add_parser("status", help="Show squad status")
    status_parser.add_argument("--config", default="squad.config.yml", help="Config file path")

    # init command
    subparsers.add_parser("init", help="Initialize squad config in current directory")

    args = parser.parse_args()

    if args.command == "run":
        config = SquadConfig.from_file(args.config)
        squad = SquadOrchestrator(config=config)
        result = squad.run(args.task)
        print(json.dumps(result, indent=2))

    elif args.command == "status":
        config = SquadConfig.from_file(args.config)
        squad = SquadOrchestrator(config=config)
        status = squad.status()
        print(json.dumps(status, indent=2))

    elif args.command == "init":
        import shutil
        import os
        template = os.path.join(os.path.dirname(__file__), "..", "squad.config.yml")
        if os.path.exists(template):
            shutil.copy(template, "squad.config.yml")
            print("✅ Initialized squad.config.yml")
        else:
            print("✅ Squad config would be created here")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()