import sys
import argparse

from automux import Automux


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="automux",
        description="a tmux session and workspace management helper",
    )

    parser.add_argument(
        "-s",
        "--session",
        type=str,
        help="Start the session using a project's path or session's registered name (using the -R option). Path must be at the root of the project.",
    )

    parser.add_argument(
        "-w",
        "--workspace",
        type=str,
        help="Start a tmux workspace containing sessions using a project's path or session's registered name (using the -R option). Path must be at the root of the project.",
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

    args = parser.parse_args()
    if args.init:
        Automux.init_config()
    elif args.create_workspace:
        Automux.create_workspace_config(args.create_workspace)
    elif args.session:
        Automux.create_session_from_config(args.session)
    elif args.workspace:
        Automux.create_workspace(args.workspace)
    elif args.list_workspaces:
        Automux.list_workspaces()
    elif args.list_sessions:
        Automux.list_sessions()
    elif args.list:
        Automux.list_sessions_and_workspaces()
    else:
        parser.print_help()

    sys.exit(0)
