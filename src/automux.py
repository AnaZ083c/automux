import textwrap
import sys
from pathlib import Path
from os import environ
from subprocess import call

from src.utils.tmux_pane import TmuxPane
from src.utils.tmux_window import TmuxWindow
from src.utils.tmux_session import TmuxSession
from src.utils.tmux_workspace import TmuxWorkspace

from src.utils.helpers import Logger

automux_env_config_path = environ.get("AUTOMUX_CONFIG", str(Path.home() / Path(".config/automux")))

global_editor = environ.get("EDITOR", "vi")


class Automux:
    def __init__(self, logger: Logger):
        self.logger = logger

        self.config_path = Path(automux_env_config_path)
        self.sessions_config = self.config_path / Path("sessions/")
        self.workspaces_config = self.config_path / Path("workspaces/")

        self.extensions = ("*.yml", "*.yaml")
        self.workspace_example = textwrap.dedent("""
            ## NOTE: This is a generated example for
            ## you to edit your workspace from
            ###
            # name: workspace_name
            #
            # sessions:
            #   - name: main_session
            #     workdir: /path/to/your/work/dir
            #     windows:
            #       - name: first_window
            #         panes:
            #           - vertical: 50
            #             cmd: echo "First pane!"
            #           - horizontal: 30
            #             cmd: echo "Second pane!"
            #           - vertical: 10
            #             cmd: echo "Third pane!"
            #         cmd: echo "First window!"
            #       - name: second_window
            #         panes:
            #           - horizontal: 50
            #           - vertical: 50
            #         cmd: echo "Second window!"
            #     start_at:
            #       window: first_window
            #       pane: 0
        """).strip()

        self.session_example = textwrap.dedent("""
            ## NOTE: This is a generated example for
            ## you to edit your session from
            ###
            # name: session_name
            #
            # windows:
            #   - name: first_window
            #     panes:
            #       - vertical: 50
            #         cmd: echo "First pane!"
            #       - horizontal: 30
            #         cmd: echo "Second pane!"
            #       - vertical: 10
            #         cmd: echo "Third pane!"
            #     cmd: echo "First window!"
            #   - name: second_window
            #     panes:
            #       - horizontal: 50
            #       - vertical: 50
            #     cmd: echo "Second window!"
            #
            # start_at:
            #   window: first_window
            #   pane: 0
        """).strip()

    def is_inited(self) -> bool:
        return self.config_path.is_dir() and self.sessions_config.is_dir() and self.workspaces_config.is_dir()

    def init_config(self) -> None:
        try:
            self.config_path.mkdir(parents=True, exist_ok=True)
            self.sessions_config.mkdir(exist_ok=True)
            self.workspaces_config.mkdir(exist_ok=True)
            self.logger.debug(f"Created automux configuration directories: {self.config_path}")
        except FileExistsError as _:
            self.logger.info("Configuration already exists, no need to recreate")

    def list_workspaces(self) -> None:
        workspaces = [w for e in self.extensions for w in self.workspaces_config.glob(e) if w.is_file()]
        print("Workspaces:")
        if len(workspaces) == 0:
            print("  No workspaces yet.")
            return
        for w in workspaces:
            if not w.is_file():
                continue
            print(f"  {w.stem}")

    def list_sessions(self) -> None:
        sessions = [s for e in self.extensions for s in self.sessions_config.glob(e) if s.is_file()]
        print("Sessions:")
        if len(sessions) == 0:
            print("  No sessions yet.")
            return
        for s in sessions:
            if not s.is_file():
                continue
            print(f"  {s.stem}")

    def list_sessions_and_workspaces(self) -> None:
        self.list_sessions()
        self.list_workspaces()

    def create_workspace_config(self, workspace_name: str) -> None:
        try:
            workspace_config_path = (self.workspaces_config / Path(workspace_name)).with_suffix(".yml")
            with open(workspace_config_path, "w") as file:
                file.write(self.workspace_example)
            self.logger.info(f"Saved workspace config to: {str(workspace_config_path)}")
        except Exception as e:
            self.logger.error(f"Error: Couldn't create config for workspace '{workspace_name}':\n {e}")
            sys.exit(1)

    def create_session_config(self, session_name: str) -> None:
        try:
            session_config_path = (self.sessions_config / Path(session_name)).with_suffix(".yml")
            with open(session_config_path, "w") as file:
                file.write(self.session_example)
            self.logger.info(f"Saved session config to: {str(session_config_path)}")
        except Exception as e:
            self.logger.error(f"Couldn't create config for session '{session_name}':\n {e}")
            sys.exit(1)

    def create_workspace(self, workspace_name: str) -> None:
        if not self.is_inited():
            self.logger.error(
                f"automux configuration not found in '{self.config_path}'\n \
                You must first create an automux config. You can do this manually or use 'automux --init'"
            )
            sys.exit(2)

        config_path = self.workspaces_config / Path(f"{workspace_name}.yml")
        tmux_workspace = TmuxWorkspace.from_config(config_path, self.logger)
        if tmux_workspace.name is None:
            self.logger.error(f"Couldn't load workspace config from this path: {config_path}")
            sys.exit(1)

        try:
            for session in tmux_workspace.sessions:
                self.create_session_from_object(tmux_session=session, auto_attach=False)
                self.logger.debug(f"Created session '{session.name}'")
        except Exception as e:
            self.logger.error(f"Something went wrong while creating workspace '{tmux_workspace.name}':\n {e}")
            sys.exit(1)

    def create_session_from_object(self, tmux_session: TmuxSession, auto_attach: bool) -> None:
        if tmux_session.name is None:
            self.logger.error("Invalid session")
            sys.exit(1)

        try:
            if not tmux_session.is_live():
                tmux_session.create()
                for i, window in enumerate(tmux_session.windows):
                    window.create(tmux_session.name, tmux_session.workdir, i)
                    assert window.name is not None

                    if window.cmd is not None:
                        window.exec_cmd(tmux_session.name)

                    if window.panes is not None:
                        for j, pane in enumerate(window.panes):
                            self.logger.debug(f"Pane position: {pane.position}, size: {pane.size}")
                            pane.create(tmux_session.name, tmux_session.workdir, window.name, j)
                            if pane.cmd is not None:
                                pane.exec_cmd(tmux_session.name, window.name, j)

                if tmux_session.start_at is not None:
                    start_window = tmux_session.start_at.get("window", 0)
                    start_pane_idx = tmux_session.start_at.get("pane", 0)

                    TmuxWindow.select(tmux_session.name, start_window, self.logger)
                    TmuxPane.select(tmux_session.name, start_window, start_pane_idx, self.logger)
            else:
                self.logger.debug(f"Session {tmux_session.name} already exists")

            if auto_attach:
                tmux_session.attach()
            self.logger.info(f"Attach to session: tmux a -t {tmux_session.name}")
        except Exception as e:
            if tmux_session.is_live():
                tmux_session.kill()
            self.logger.error(f"Something went wrong while creating session '{tmux_session.name}':\n {e}")
            sys.exit(1)

    def create_session_from_config(self, session_name: str) -> None:
        if not self.is_inited():
            self.logger.debug(
                f"automux configuration not found in '{self.config_path}'\n \
                You must first create an automux config. You can do this manually or use 'automux --init'"
            )
            sys.exit(2)

        tmux_session = TmuxSession.from_config(
            str(self.sessions_config / Path(f"{session_name}.yml")), logger=self.logger
        )
        self.create_session_from_object(tmux_session=tmux_session, auto_attach=False)

    @staticmethod
    def _config_is_session(config_path: Path) -> bool:
        return False

    @staticmethod
    def _config_is_workspace(config_path: Path) -> bool:
        return False

    def edit(self, config_name: str, is_workspace: bool) -> None:
        if not self.is_inited():
            self.logger.error(
                f"automux configuration not found in '{self.config_path}'\n \
                You must first create an automux config. You can do this manually or use 'automux --init'"
            )
            sys.exit(2)

        config_path = self.workspaces_config if is_workspace else self.sessions_config
        config_path = config_path / Path(f"{config_name}.yml")
        if not config_path.exists():
            self.logger.error(
                f"{'Workspace' if is_workspace else 'Session'} '{config_name}' does not exist in the configuration"
            )
            sys.exit(2)

        # Open with $EDITOR
        with open(config_path) as f:
            call([global_editor, f.name])
