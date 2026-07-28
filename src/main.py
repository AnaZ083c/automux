import sys
import argparse

from src.automux import Automux, Logger


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="automux",
        description="a tmux session and workspace management helper",
    )

    parser.add_argument(
        "-s",
        "--session",
        type=str,
        help="Start the session with the given name; e.g. you have a config 'mysession.yml', to start: 'automux -w mysession'",
    )

    parser.add_argument(
        "-w",
        "--workspace",
        type=str,
        help="Start a tmux workspace with the given name; e.g. you have a config 'myworkspace.yml', to start: 'automux -w myworkspace'",
    )

    parser.add_argument(
        "-cw",
        "--create-workspace",
        type=str,
        help="Create a tmux workspace config file (comes with a commented example)",
    )

    parser.add_argument(
        "-cs",
        "--create-session",
        type=str,
        help="Create a tmux session config file (comes with a commented example)",
    )

    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="Init automux configuration: '~/.config/automux/'",
    )

    parser.add_argument(
        "-lw",
        "--list-workspaces",
        action="store_true",
        help="List all workspaces (the file names in your configs).",
    )

    parser.add_argument(
        "-ls",
        "--list-sessions",
        action="store_true",
        help="List all sessions (the file names in your configs).",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all sessions and workspaces (the file names in your configs).",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print all steps into the terminal (useful for debugging).",
    )

    args = parser.parse_args()
    logger = Logger(verbose=args.verbose)
    automux = Automux(logger=logger)
    if args.init:
        automux.init_config()
    elif args.create_workspace:
        automux.create_workspace_config(args.create_workspace)
    elif args.session:
        automux.create_session_from_config(args.session)
    elif args.workspace:
        automux.create_workspace(args.workspace)
    elif args.list_workspaces:
        automux.list_workspaces()
    elif args.list_sessions:
        automux.list_sessions()
    elif args.list:
        automux.list_sessions_and_workspaces()
    else:
        parser.print_help()

    sys.exit(0)


if __name__ == "__main__":
    main()
