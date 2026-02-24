import yaml
from pathlib import Path

from subprocess import run, CalledProcessError, check_output, DEVNULL
from typing import Any

from utils.tmux_window import TmuxWindow


class TmuxSession:
    def __init__(
        self,
        name: str | None = None,
        workdir: str | None = None,
        windows: list[TmuxWindow] | None = None,
        start_at: dict[str, Any] | None = None,
    ):
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
    def from_config(filename: str) -> "TmuxSession":
        if not Path(filename).is_file():
            raise Exception(f"Config is nowhere to be found: {filename}")
        try:
            print(f"Info: Getting session data from config {filename}")
            with open(filename, "r") as file:
                config = yaml.safe_load(file)

            return TmuxSession.from_dict(session=config)
        except Exception as e:
            raise Exception(f"Couldn't get config: {e}")

    @staticmethod
    def from_dict(session: dict[str, Any]) -> "TmuxSession":
        if "name" not in session:
            raise Exception("Invalid session configuration. Missing required option 'name'")

        try:
            tmux_session = TmuxSession(
                name=session["name"],
                workdir=session.get("workdir", None),
                windows=[],
                start_at=session.get("start_at", None),
            )

            windows = session["windows"]
            for w in windows:
                tmux_window = TmuxWindow(
                    name=w["name"],
                    cmd=w.get("cmd", None),
                    panes=w.get("panes", None),
                )
                tmux_session.windows.append(tmux_window)

            print(f"WORKDIR: {tmux_session.workdir}")
            return tmux_session
        except Exception as e:
            raise Exception(f"Couldn't process session configuration: {e}")

    def create(self) -> None:
        try:
            if self.name is None:
                raise Exception("Missing session name in your session config")

            print(f"Info: Creating session {self.name} in working directory in '{self.workdir}'")
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
            print(f"Info: Attaching to session: {self.name}")
            run(["tmux", "attach-session", "-t", f"{self.name}:0"])
        except CalledProcessError as e:
            raise Exception(f"Failed to create session {self.name}: {e}")

    def kill(self) -> None:
        try:
            print(f"Info: Killing session: {self.name}")
            run(["tmux", "kill-session", "-t", f"{self.name}"])
        except CalledProcessError as e:
            raise Exception(f"Failed to kill session {self.name}: {e}")
