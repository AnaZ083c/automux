import pytest

import textwrap

@pytest.fixture(name="all_options_config")
def fixture_all_options_config() -> str:
    return {
        "name": "MyTestSession",
        "windows": [
            {
                "name": "first_test_window",
                "panes": [
                    {
                        "vertical": 50,
                        "cmd": "echo 'first test pane'",
                    },
                    {
                        "horizontal": 30,
                        "cmd": "echo 'second test pane'",
                    },
                ],
                "cmd": "echo 'first test window'",
            },
            {
                "name": "second_test_window",
                "panes": [
                    {
                        "horizontal": 50,
                    },
                    {
                        "vertical": 50,
                    },
                ],
                "cmd": "echo 'second test window'",
            },
        ],
        "start_at": {
            "window": "first_test_window",
            "pane": 0,
        },
    }
