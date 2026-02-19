from subprocess import run, CalledProcessError
from typing import Any

from utils.tmux_pane import TmuxPane


class TmuxWindow:
    def __init__(
        self,
        name: str | None = None,
        cmd: str | None = None,
        panes: list[dict[str, Any]] | None = None,
    ):
        self.name = name
        self.cmd = cmd
        self.panes = self.get_panes(panes)

    @classmethod
    def select(
        cls,
        session_name: str,
        window_name: str | int,
    ) -> None:
        try:
            print(f"Info: Selected window: {session_name}:{window_name}")
            run(["tmux", "select-window", "-t", f"{session_name}:{window_name}"])
        except CalledProcessError as e:
            raise Exception(f"Failed to select window: {session_name}:{window_name}, error: {e}")

    def get_panes(
        self,
        panes_dicts: list[dict[str, Any]] | None,
    ) -> list[TmuxPane] | None:
        tmux_panes = []
        if panes_dicts is None:
            print("Info: No panes in this window.")
            return None

        for pane in panes_dicts:
            tmux_pane = TmuxPane()
            for key, value in pane.items():
                if key in ("horizontal", "vertical"):
                    tmux_pane.position = key
                    tmux_pane.size = pane[key]
                elif key in ("cmd"):
                    tmux_pane.cmd = pane[key]
            tmux_panes.append(tmux_pane)

        return tmux_panes

    def exec_cmd(self, session_name: str) -> None:
        try:
            assert self.cmd is not None
            print(f"Info: Executing command: {self.cmd}")
            run(["tmux", "send-keys", "-t", f"{session_name}:{self.name}", self.cmd, "C-m"])
        except CalledProcessError as e:
            raise Exception(f"Failed to execute the command: {self.cmd}, error: {e}")

    def create(self, session_name: str, index: int) -> None:
        try:
            assert self.name is not None
            print(f"Info: Creating a new window {self.name} at index {index}")
            if index == 0:
                run(["tmux", "rename-window", "-t", f"{session_name}:{index}", self.name])
            else:
                run(["tmux", "new-window", "-t", f"{session_name}:{index}", "-n", self.name])
        except CalledProcessError as e:
            raise Exception(f"Failed to create window at index {index}: {e}")
