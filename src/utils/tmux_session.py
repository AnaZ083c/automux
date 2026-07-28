import yaml
from pathlib import Path

from subprocess import run, CalledProcessError, check_output, DEVNULL
from typing import Any

from src.utils.tmux_window import TmuxWindow
from src.utils.helpers import Logger


class TmuxSession:
    def __init__(
        self,
        logger: Logger,
        name: str | None = None,
        workdir: str | None = None,
        windows: list[TmuxWindow] | None = None,
        start_at: dict[str, Any] | None = None,
    ):
        self.logger = logger
        self.name = name
        self.workdir = str(Path(workdir if workdir is not None else Path.cwd()).expanduser())
        self.windows = windows if windows is not None else []
        self.start_at = start_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "windows": [w.to_dict() for w in self.windows],
            "start_at": self.start_at,
        }

    @staticmethod
    def from_config(filename: str, logger: Logger) -> "TmuxSession":
        if not Path(filename).is_file():
            raise Exception(f"Config is nowhere to be found: {filename}")
        try:
            logger.debug(f"Getting session data from config {filename}")
            with open(filename, "r") as file:
                config = yaml.safe_load(file)

            return TmuxSession.from_dict(session=config, logger=logger)
        except Exception as e:
            raise Exception(f"Couldn't get config: {e}")

    @staticmethod
    def from_dict(session: dict[str, Any], logger: Logger) -> "TmuxSession":
        if "name" not in session:
            raise Exception("Invalid session configuration. Missing required option 'name'")

        try:
            tmux_session = TmuxSession(
                logger=logger,
                name=session["name"],
                workdir=session.get("workdir", None),
                windows=[],
                start_at=session.get("start_at", None),
            )

            windows = session["windows"]
            for w in windows:
                tmux_window = TmuxWindow(
                    logger=logger,
                    name=w["name"],
                    cmd=w.get("cmd", None),
                    panes=w.get("panes", None),
                )
                tmux_session.windows.append(tmux_window)
            return tmux_session
        except Exception as e:
            raise Exception(f"Couldn't process session configuration: {e}")

    def create(self) -> None:
        try:
            if self.name is None:
                raise Exception("Missing session name in your session config")

            self.logger.debug(f"Creating session {self.name} in working directory in '{self.workdir}'")
            run(["tmux", "new-session", "-d", "-s", self.name, "-c", self.workdir], check=True)
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")

    def is_live(self) -> bool:
        try:
            if self.name is None:
                raise Exception("Missing session name in your session config")

            check_output(["tmux", "has-session", "-t", self.name], stderr=DEVNULL, text=True)
        except CalledProcessError:
            return False

        return True

    def attach(self) -> None:
        try:
            self.logger.debug(f"Attaching to session: {self.name}")
            run(["tmux", "attach-session", "-t", f"{self.name}:0"])
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")

    def kill(self) -> None:
        try:
            self.logger.debug(f"Killing session: {self.name}")
            run(["tmux", "kill-session", "-t", f"{self.name}"])
        except CalledProcessError as e:
            raise Exception(f"Failed to kill session {self.name}: {e}")
