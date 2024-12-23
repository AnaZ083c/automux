import pytest  # noqa: F401

from automux.utils.tmux import Tmux


class TestTmux:
    def test_get_version(self):
        version = Tmux.get_version()
        assert "tmux 3." in version
