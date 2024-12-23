import pytest  # noqa: F401

from pytest_mock import MockFixture
from automux.utils.tmux_session import TmuxSession

from typing import Any


class TestTmuxSession:
    def test_get_from_config_all(self, mocker: MockFixture, all_options_config: dict[str, Any]):
        mocker.patch("pathlib.Path.is_file", return_value=True)

        mock_open = mocker.patch("builtins.open",
            mocker.mock_open(read_data="test confing")
        )

        mocker.patch("yaml.safe_load", return_value=all_options_config)
        
        __import__('pprint').pprint(all_options_config)
        result = TmuxSession.get_from_config("session.yml")
        
        assert result.__class__ == TmuxSession
        assert result.name == all_options_config["name"]
        assert len(result.windows) == len(all_options_config["windows"])
        assert result.start_at == all_options_config["start_at"]
