import argparse

from automux.utils.tmux_pane import TmuxPane
from automux.utils.tmux_window import TmuxWindow
from automux.utils.tmux_session import TmuxSession


AUTOMUX_CACHE_PATH = "~/.cache/automux/sessions.yml"


def main(project_root_path: str) -> None:
    try:
        if project_root_path[len(project_root_path) - 1] == "/":
            project_root_path = project_root_path[: len(project_root_path) - 1]

        tmux_session = TmuxSession.get_from_config(f"{project_root_path}/.tmux/session.yml")
        assert tmux_session.name is not None

        if not tmux_session.is_live():
            tmux_session.create()
            for i, window in enumerate(tmux_session.windows):
                window.create(tmux_session.name, i)
                assert window.name is not None

                if window.cmd is not None:
                    window.exec_cmd(tmux_session.name)

                if window.panes is not None:
                    for j, pane in enumerate(window.panes):
                        print(f"Pane position: {pane.position}, size: {pane.size}")
                        pane.create(tmux_session.name, window.name, j)
                        if pane.cmd is not None:
                            pane.exec_cmd(tmux_session.name, window.name, j)

            if tmux_session.start_at is not None:
                start_window = tmux_session.start_at["window"] if "window" in tmux_session.start_at else 0
                start_pane_idx = tmux_session.start_at["pane"] if "pane" in tmux_session.start_at else 0

                TmuxWindow.select(tmux_session.name, start_window)
                TmuxPane.select(tmux_session.name, start_window, start_pane_idx)
        else:
            print(f"Session {tmux_session.name} already exists")

        tmux_session.attach()
    except Exception as e:
        if tmux_session.is_live():
            tmux_session.kill()
        print(f"ERROR: {e}")


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
    main(args.start)
else:
    parser.print_help()
