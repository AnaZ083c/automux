import sys
from pathlib import Path

from utils.tmux_pane import TmuxPane
from utils.tmux_window import TmuxWindow
from utils.tmux_session import TmuxSession


AUTOMUX_CACHE_PATH = "~/.cache/automux/sessions.yml"


class Automux:

    @classmethod
    def create_session(cls, config_path: Path) -> None:
        tmux_session = TmuxSession.get_from_config(f"{config_path}/.tmux/session.yml")
        if tmux_session.name is None:
            print(f"Error: Couldn't load session config from this path: {config_path}")
            sys.exit(1)

        assert tmux_session.name is not None

        try:
            # check if config_path has session.yml in there
            # check if conifg_path is a directory

            if config_path[len(config_path) - 1] == "/":
                config_path = config_path[: len(config_path) - 1]

            if not tmux_session.is_live():
                tmux_session.create()
                for i, window in enumerate(tmux_session.windows):
                    window.create(tmux_session.name, i)
                    assert window.name is not None

                    if window.cmd is not None:
                        window.exec_cmd(tmux_session.name)

                    if window.panes is not None:
                        for j, pane in enumerate(window.panes):
                            print(f"Info: Pane position: {pane.position}, size: {pane.size}")
                            pane.create(tmux_session.name, window.name, j)
                            if pane.cmd is not None:
                                pane.exec_cmd(tmux_session.name, window.name, j)

                if tmux_session.start_at is not None:
                    start_window = tmux_session.start_at["window"] if "window" in tmux_session.start_at else 0
                    start_pane_idx = tmux_session.start_at["pane"] if "pane" in tmux_session.start_at else 0

                    TmuxWindow.select(tmux_session.name, start_window)
                    TmuxPane.select(tmux_session.name, start_window, start_pane_idx)
            else:
                print(f"Info: Session {tmux_session.name} already exists")

            tmux_session.attach()
        except Exception as e:
            if tmux_session.is_live():
                tmux_session.kill()
            print(f"Error: {e}")
