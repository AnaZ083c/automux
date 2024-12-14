from subprocess import run, CalledProcessError, check_output, Popen, PIPE, STDOUT, DEVNULL
from enum import Enum

from utils.tmux import Tmux
from utils.tmux_pane import TmuxPane


class TmuxWindow:
    def __init__(
        self,
        name: str = None,
        cmd: str = None,
        panes: list = None
    ):
        self.name = name
        self.cmd = cmd
        self.panes = self.get_panes(panes)


    @classmethod
    def select(cls, session_name: str, window_name: str) -> None:
        try:
            print(f"Selected window: {session_name}:{window_name}")
            run(['tmux', 'select-window', '-t', f'{session_name}:{window_name}'])
        except CalledProcessError as e:
            raise Exception(f"Failed to select window: {session_name}:{window_name}, error: {e}")


    def get_panes(self, panes_dicts: list[dict[str, any]]) -> list[TmuxPane]:
        tmux_panes = []
        if panes_dicts is None:
            print(f"No panes in this window.")
            return None

        for pane in panes_dicts:
            tmux_pane = TmuxPane()
            for key, value in pane.items():
                if key in ('horizontal', 'vertical'):
                    tmux_pane.position = key
                    tmux_pane.size = pane[key]
                elif key in ('cmd'):
                    tmux_pane.cmd = pane[key]
            tmux_panes.append(tmux_pane)

        return tmux_panes


    def exec_cmd(self, session_name: str) -> None:
        try:
            print(f"Executing command: {self.cmd}")
            run(['tmux', 'send-keys', '-t', f'{session_name}:{self.name}', self.cmd, 'C-m'])
        except CalledProcessError as e:
            raise Exception(f"Failed to execute the command: {self.cmd}, error: {e}")


    def create(self, session_name: str, index: int) -> None:
        try:
            print(f"Creating a new window {self.name} at index {index}")
            if index == 0:
                run(['tmux', 'rename-window', '-t', f'{session_name}:{index}', self.name])
            else:
                run(['tmux', 'new-window', '-t', f'{session_name}:{index}', '-n', self.name])
        except CalledProcessError as e:
            raise Exception(f"Failed to create window at index {index}: {e}")

