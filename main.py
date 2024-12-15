from automux.utils.tmux_pane import TmuxPane
from automux.utils.tmux_window import TmuxWindow
from automux.utils.tmux_session import TmuxSession


try:
    tmux_session = TmuxSession.get_from_config(".tmux/session.yml")
    assert tmux_session.name is not None

    if not tmux_session.is_live():
        tmux_session.create()
        for i, window in enumerate(tmux_session.windows):
            window.create(tmux_session.name, i)
            assert window.name is not None

            if window.cmd is not None:
                window.exec_cmd(tmux_session.name)

            if window.panes is not None:
                for j, pane in enumerate(window.panes):
                    print(f"Pane position: {pane.position}, size: {pane.size}")
                    pane.create(tmux_session.name, window.name, j)
                    if pane.cmd is not None:
                        pane.exec_cmd(tmux_session.name, window.name, j)

        if tmux_session.start_at is not None:
            start_window = tmux_session.start_at["window"] if "window" in tmux_session.start_at else 0
            start_pane_idx = tmux_session.start_at["pane"] if "pane" in tmux_session.start_at else 0

            TmuxWindow.select(tmux_session.name, start_window)
            TmuxPane.select(tmux_session.name, start_window, start_pane_idx)
    else:
        print(f"Session {tmux_session.name} already exists")

    tmux_session.attach()
except Exception as e:
    if tmux_session.is_live():
        tmux_session.kill()
    print(f"ERROR: {e}")
