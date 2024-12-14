from subprocess import run, CalledProcessError, check_output, Popen, PIPE, STDOUT, DEVNULL
from enum import Enum

from utils.tmux import Tmux


class TmuxPane:
    def __init__(
        self,
        position: str = None,
        size: int = None,
        cmd: str = None,
    ):
        self.position = position
        self.size = size
        self.cmd = cmd

    @classmethod
    def select(cls, session_name: str, window_name: str, pane_idx: int) -> None:
        try:
            print(f"Selected pane: {session_name}:{window_name}.{pane_idx}")
            run(['tmux', 'select-pane', '-t', f'{session_name}:{window_name}.{pane_idx}'])
        except CalledProcessError as e:
            raise Exception(f"Failed to select pane: {session_name}:{window_name}.{pane_idx}, error: {e}")


    def exec_cmd(self, session_name: str, window_name: str, index: int) -> bool:
        try:
            print(f"Executing command on window {window_name}.{index}: {self.cmd}")
            run(['tmux', 'send-keys', '-t', f'{session_name}:{window_name}.{index}', self.cmd, 'C-m'])
        except CalledProcessError as e:
            raise Exception(f"Failed to execute the command: {self.cmd}, error: {e}")


    def create(
        self,
        session_name: str,
        window_name: str,
        index: int,
    ) -> None:
        tmux_version = Tmux.get_version()

        try:
            pane_position = '-h' if self.position == 'horizontal' else '-v'
            pane_splitter = '-p' if '3.0' in tmux_version else '-l'
            size = f'{self.size}' if '3.0' in tmux_version else f'{self.size}%'

            run(['tmux', 'split-window', '-t', f'{session_name}:{window_name}.{index}', pane_position, pane_splitter, size])
        except CalledProcessError as e:
            raise Exception(f"Failed to create a pane: {session_name}:{window_name}.{index}, error: {e}")

