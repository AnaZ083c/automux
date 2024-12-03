import yaml
import pathlib

from subprocess import run, CalledProcessError, check_output, Popen, PIPE, STDOUT, DEVNULL


class TmuxWindow:
    def __init__(self, name: str = None, cmd: str = None):
        self.name = name
        self.cmd = cmd


    def exec_cmd(self, session_name) -> bool:
        try:
            print(f"Executing command: {self.cmd}")
            run(['tmux', 'send-keys', '-t', f'{session_name}:{self.name}', self.cmd, 'C-m'])
        except CalledProcessError as e:
            raise Exception(f"Failed to execute the command: {self.cmd}, error: {e}")

        return True


    def create(self, session_name: str, index: int) -> bool:
        try:
            print(f"Creating a new window {self.name} at index {index}")
            if index == 0:
                run(['tmux', 'rename-window', '-t', f'{session_name}:{index}', self.name])
            else:
                run(['tmux', 'new-window', '-t', f'{session_name}:{index}', '-n', self.name])
        except CalledProcessError as e:
            raise Exception(f"Failed to create window at index {index}: {e}")

        return True


class TmuxSession:
    def __init__(self, name: str = None, windows: list = []):
        self.name = name
        self.windows = windows


    @staticmethod
    def get_from_config(filename: str) -> 'TmuxSession':
        if not pathlib.Path(filename).is_file():
            raise Exception("Config is nowhere to be found")
        try:
            print(f"Getting session data from config {filename}")
            with open(filename, 'r') as file:
                config = yaml.safe_load(file)

            tmux_session = TmuxSession()
            tmux_session.name = config["name"]

            windows = config["windows"]

            for w in windows:
                tmux_window = TmuxWindow(
                    name=w["name"],
                    cmd=w["cmd"] if "cmd" in w else None,
                )

                tmux_session.windows.append(tmux_window)

            print(f"Retrieved all data")
            return tmux_session
        except Exception as e:
            raise Exception(f"Couldn't get config: {e}")

    
    def create(self) -> bool:
        try:
            print(f"Creating session {self.name}")
            run(['tmux', 'new-session', '-d', '-s', self.name])
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")

        return True

    
    def is_live(self) -> bool:
        try:
            result = check_output(['tmux', 'has-session', '-t', self.name], stderr=DEVNULL, text=True)
        except CalledProcessError as e:
            return False
        
        return True


    def attach(self) -> bool:
        try:
            print(f"Attaching to session: {self.name}")
            run(['tmux', 'attach-session', '-t', f'{self.name}:0'])
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")

        return True


try:
    tmux_session = TmuxSession.get_from_config('.tmux/session.yml')

    if not tmux_session.is_live():
        tmux_session.create()
        for idx, window in enumerate(tmux_session.windows):
            window.create(tmux_session.name, idx)
            if window.cmd is not None:
                window.exec_cmd(tmux_session.name)
    else:
        print(f"Session {tmux_session.name} already exists")

    tmux_session.attach()
except Exception as e:
    print(f"ERROR: {e}")
