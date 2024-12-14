import yaml
import pathlib

from subprocess import run, CalledProcessError, check_output, Popen, PIPE, STDOUT, DEVNULL

from utils.tmux_window import TmuxWindow


class TmuxSession:
    def __init__(
        self,
        name: str = None,
        windows: list[TmuxWindow] = [],
        start_at: dict[str, any] = None,
    ):
        self.name = name
        self.windows = windows
        self.start_at = start_at


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

            tmux_session.start_at = config["start_at"] if "start_at" in config else None

            windows = config["windows"]

            for w in windows:
                tmux_window = TmuxWindow(
                    name=w["name"],
                    cmd=w["cmd"] if "cmd" in w else None,
                    panes=w["panes"] if "panes" in w else None,
                )

                tmux_session.windows.append(tmux_window)

            print(f"Retrieved all data")
            return tmux_session
        except Exception as e:
            raise Exception(f"Couldn't get config: {e}")

    
    def create(self) -> None:
        try:
            print(f"Creating session {self.name}")
            run(['tmux', 'new-session', '-d', '-s', self.name])
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")

    
    def is_live(self) -> bool:
        try:
            result = check_output(['tmux', 'has-session', '-t', self.name], stderr=DEVNULL, text=True)
        except CalledProcessError as e:
            return False
        
        return True


    def attach(self) -> None:
        try:
            print(f"Attaching to session: {self.name}")
            run(['tmux', 'attach-session', '-t', f'{self.name}:0'])
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")


    def kill(self) -> None:
        try:
            print(f"Killing session: {self.name}")
            run(['tmux', 'kill-session', '-t', f'{self.name}'])
        except CalledProcessError as e:
            raise Exception(f"Failed to kill session {self.name}: {e}")


