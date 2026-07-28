import yaml
import pathlib

from subprocess import CalledProcessError
from typing import Any

from src.utils.tmux_session import TmuxSession
from src.utils.helpers import Logger


class TmuxWorkspace:
    def __init__(self, logger: Logger, name: str, sessions: list[TmuxSession]):
        self.logger = logger
        self.name = name
        self.sessions = sessions

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "sessions": [s.to_dict() for s in self.sessions]}

    @staticmethod
    def from_config(config: pathlib.Path, logger: Logger) -> "TmuxWorkspace":
        if not config.is_file():
            raise Exception(f"Config is nowhere to be found: {str(config)}")
        try:
            logger.debug(f"Getting workspace data from config {str(config)}")
            with open(str(config), "r") as file:
                config_content = yaml.safe_load(file)

            if "name" not in config_content:
                raise Exception(f"'name' is required: {str(config)}")

            if "sessions" not in config_content:
                raise Exception(f"'sessions' is required: {str(config)}")

            tmux_sessions: list[TmuxSession] = [
                TmuxSession.from_dict(session, logger) for session in config_content["sessions"]
            ]

            return TmuxWorkspace(
                logger=logger,
                name=config_content["name"],
                sessions=tmux_sessions,
            )
        except Exception as e:
            raise Exception(f"Couldn't process session configuration: {e}")

    def create(self) -> None:
        try:
            self.logger.debug(f"Creating workspace {self.name}")
            for session in self.sessions:
                session.create()
        except CalledProcessError as e:
            raise Exception(f"Failed to create workspace {self.name}: {e}")
