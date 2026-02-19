import argparse

from utils.tmux_pane import TmuxPane
from utils.tmux_window import TmuxWindow
from utils.tmux_session import TmuxSession
from automux import Automux


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="automux", description="a tmux session configurator for every project")

    parser.add_argument(
        "-r",
        "--register",
        type=str,
        help="Register the project's session config at a given path for the future use. This will store the path of a project's session config for a quicker access from anywhere.",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=str,
        help="Start the session using a project's path or session's registered name (using the -R option). Path must be at the root of the project.",
    )
    parser.add_argument(
        "-R",
        "--registered",
        action="store_true",
        help="Mark session as registered.",
    )
    parser.add_argument(
        "-l",
        "--list-registered",
        action="store_true",
        help="List all registered session configs; projects.",
    )

    args = parser.parse_args()
    if args.start:
        Automux.create_session(args.start)
    else:
        parser.print_help()
