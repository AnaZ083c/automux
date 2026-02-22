import yaml
import pathlib

from subprocess import CalledProcessError
from typing import Any

from utils.tmux_session import TmuxSession


class TmuxWorkspace:
    def __init__(self, name: str, sessions: list[TmuxSession]):
        self.name = name
        self.sessions = sessions

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "sessions": [s.to_dict() for s in self.sessions]}

    @staticmethod
    def from_config(config: pathlib.Path) -> "TmuxWorkspace":
        if not config.is_file():
            raise Exception(f"Config is nowhere to be found: {str(config)}")
        try:
            print(f"Info: Getting workspace data from config {str(config)}")
            with open(str(config), "r") as file:
                config = yaml.safe_load(file)

            if "name" not in config:
                raise Exception(f"Error: 'name' is required: {str(config)}")

            if "sessions" not in config:
                raise Exception(f"Error: 'sessions' is required: {str(config)}")

            tmux_sessions: list[TmuxSession] = [TmuxSession.from_dict(session) for session in config["sessions"]]

            return TmuxWorkspace(
                name=config["name"],
                sessions=tmux_sessions,
            )
        except Exception as e:
            raise Exception(f"Couldn't process session configuration: {e}")

    def create(self) -> None:
        try:
            print(f"Info: Creating workspace {self.name}")
            for session in self.sessions:
                session.create()
        except CalledProcessError as e:
            raise Exception(f"Failed to create workspace {self.name}: {e}")
