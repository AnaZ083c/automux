import textwrap
import sys
from pathlib import Path

from utils.tmux_pane import TmuxPane
from utils.tmux_window import TmuxWindow
from utils.tmux_session import TmuxSession
from utils.tmux_workspace import TmuxWorkspace


# TODO: is this still needed?
AUTOMUX_CACHE_PATH = "~/.cache/automux/sessions.yml"


class Automux:
    config_path = Path("~/.config/automux")
    sessions_config = config_path / Path("sessions/")
    workspaces_config = config_path / Path("workspaces/")

    extensions = ("*.yml", "*.yaml")
    workspace_example = textwrap.dedent("""
        ## NOTE: This is a generated example for
        ## you to edit your workspace from
        ###
        # name: WorkspaceName
        #
        # sessions:
        #   - name: MyMainSession
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
        #
        #   - name: MyHelperSession
        #     windows:
        #       - name: helper_first_window
        #         panes:
        #           - vertical: 50
        #             cmd: echo "First pane 123!"
        #           - horizontal: 30
        #             cmd: echo "Second pane 123!"
        #           - vertical: 10
        #             cmd: echo "Third pane 123!"
        #         cmd: echo "First window 123!"
        #       - name: helper_second_window
        #         panes:
        #           - horizontal: 50
        #           - vertical: 50
        #         cmd: echo "Second window 123!"
        #     start_at:
        #       window: helper_first_window
        #       pane: 0
    """).strip()

    session_example = textwrap.dedent("""
        ## NOTE: This is a generated example for
        ## you to edit your session from
        ###
        # name: SessionName
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

    @classmethod
    def is_inited(cls) -> bool:
        return cls.config_path.is_dir() and cls.sessions_config.is_dir() and cls.workspaces_config.is_dir()

    @classmethod
    def init_config(cls) -> None:
        try:
            cls.config_path.mkdir(parents=True, exist_ok=True)
            cls.sessions_config.mkdir(exist_ok=True)
            cls.workspaces_config.mkdir(exist_ok=True)
            print(f"Info: Created automux configuration directories: {cls.config_path}")
        except FileExistsError as _:
            print("Info: configuration already exists, no need to recreate")

    @classmethod
    def list_workspaces(cls) -> None:
        workspaces = [w for e in cls.extensions for w in cls.workspaces_config.glob(e) if w.is_file()]
        print("Workspaces:")
        for w in workspaces:
            if not w.is_file():
                continue
            print(f"\t{w.stem}")

    @classmethod
    def list_sessions(cls) -> None:
        sessions = [s for e in cls.extensions for s in cls.sessions_config.glob(e) if s.is_file()]
        print("Sessions:")
        for s in sessions:
            if not s.is_file():
                continue
            print(f"\t{s.stem}")

    @classmethod
    def list_sessions_and_workspaces(cls) -> None:
        cls.list_sessions()
        print("\n")
        cls.list_workspaces()

    @classmethod
    def create_workspace_config(cls, workspace_name: str) -> None:
        try:
            workspace_config_path = (cls.workspaces_config / Path(workspace_name)).with_suffix(".yml")
            with open(workspace_config_path, "w") as file:
                file.write(cls.workspace_example)
            print(f"Info: Saved workspace config to: {str(workspace_config_path)}")
        except Exception as e:
            print(f"Error: Couldn't create config for workspace '{workspace_name}':\n {e}")
            sys.exit(1)

    @classmethod
    def create_session_config(cls, session_name: str) -> None:
        try:
            session_config_path = (cls.sessions_config / Path(session_name)).with_suffix(".yml")
            with open(session_config_path, "w") as file:
                file.write(cls.session_example)
            print(f"Info: Saved session config to: {str(session_config_path)}")
        except Exception as e:
            print(f"Error: Couldn't create config for session '{session_name}':\n {e}")
            sys.exit(1)

    @classmethod
    def create_workspace(cls, workspace_name: str) -> None:
        if not cls.is_inited():
            print(f"Error: automux configuration not found in '{cls.config_path}'\n ",
                  "You must first create an automux config. You can do this manually or use 'automux --init'")
            sys.exit(2)

        config_path = cls.workspaces_config / Path(f"{workspace_name}.yml")
        tmux_workspace = TmuxWorkspace.from_config(config_path)
        if tmux_workspace.name is None:
            print(f"Error: Couldn't load workspace config from this path: {config_path}")
            sys.exit(1)

        try:
            for session in tmux_workspace.sessions:
                cls.create_session_from_object(tmux_session=session)
                print(f"Info: Created session '{session.name}'\n")
        except Exception as e:
            print(f"Error: Something went wrong while creating workspace '{tmux_workspace.name}':\n {e}")
            sys.exit(1)

    @classmethod
    def create_session_from_object(cls, tmux_session: TmuxSession) -> None:
        if tmux_session.name is None:
            print("Error: Invalid session")
            sys.exit(1)

        try:
            if not tmux_session.is_live():
                tmux_session.create()
                for i, window in enumerate(tmux_session.windows):
                    window.create(tmux_session.name, i)
                    assert window.name is not None

                    if window.cmd is not None:
                        window.exec_cmd(tmux_session.name)

                    if window.panes is not None:
                        for j, pane in enumerate(window.panes):
                            print(f"Info: Pane position: {pane.position}, size: {pane.size}")
                            pane.create(tmux_session.name, window.name, j)
                            if pane.cmd is not None:
                                pane.exec_cmd(tmux_session.name, window.name, j)

                if tmux_session.start_at is not None:
                    start_window = tmux_session.start_at.get("window", 0)
                    start_pane_idx = tmux_session.start_at.get("pane", 0)

                    TmuxWindow.select(tmux_session.name, start_window)
                    TmuxPane.select(tmux_session.name, start_window, start_pane_idx)
            else:
                print(f"Info: Session {tmux_session.name} already exists")

            tmux_session.attach()
        except Exception as e:
            if tmux_session.is_live():
                tmux_session.kill()
            print(f"Error: Something went wrong while creating session '{tmux_session.name}':\n {e}")
            sys.exit(1)

    @classmethod
    def create_session_from_config(cls, session_name: str) -> None:
        if not cls.is_inited():
            print(f"Error: automux configuration not found in '{cls.config_path}'\n ",
                  "You must first create an automux config. You can do this manually or use 'automux --init'")
            sys.exit(2)

        tmux_session = TmuxSession.from_config(cls.sessions_config / Path(f"{session_name}.yml"))
        cls.create_session_from_object(tmux_session=tmux_session)
