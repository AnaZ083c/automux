# Automux - manage Tmux sessions and workspaces

## Requirements
1. Tmux 3.4+
    * 3.6a works as well but didn't test on other versions so, if you have any other version, know that it might not work properly there.
2. Python 3.12
3. environment:
```shell
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Installation
```shell
make build

# in your .bashrc (or whatever other shell config)
export PATH=$PATH:"path/to/automux/repo/dist"

# apply changes
source ~/.bashrc  # or restart your terminal

# test installation
automux
```

## How to use
```console
$ automux
usage: automux [-h] [-s SESSION] [-w WORKSPACE] [-cw CREATE_WORKSPACE] [-cs CREATE_SESSION] [-i] [-lw] [-ls] [-l]

a tmux session and workspace management helper

options:
  -h, --help            show this help message and exit
  -s, --session SESSION
                        Start the session using a project's path or session's registered name (using the -R option). Path must be at the root of
                        the project.
  -w, --workspace WORKSPACE
                        Start a tmux workspace containing sessions using a project's path or session's registered name (using the -R option).
                        Path must be at the root of the project.
  -cw, --create-workspace CREATE_WORKSPACE
                        Create a tmux workspace config file (comes with a commented example)
  -cs, --create-session CREATE_SESSION
                        Create a tmux session config file (comes with a commented example)
  -i, --init            Init automux configuration: '~/.config/automux/'
  -lw, --list-workspaces
                        List all workspaces (the file names in your configs).
  -ls, --list-sessions  List all sessions (the file names in your configs).
  -l, --list            List all sessions and workspaces (the file names in your configs).
```

### Session config

> [!NOTE]
> Your session configuration should be in `~/.config/automux/sessions/`. See `automux --help` for more info.


| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `name` | `str` | Name of the session | no |
| `workdir` | `str` | Session's working directory. If not set, default will be the directory from where `automux` was called from | yes |
| `windows` | `list(dict)` | List of windows to be created in the session | yes |
| `start_at` | `dict` | Name of the starting window and index of the starting pane (on attach) | yes |


#### `windows` options

| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `name` | `str` | Name of the window in a session | no |
| `cmd` | `str` | A command to be executed in this window | yes |
| `panes` | `list(dict)` | List of panes to be created in the window (splitting the window) | yes |


#### `panes` options

| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `vertical` | `int` | Split window vertically by a percentage | no |
| `horizontal` | `int` | Split window horizontally by a percentage | no |
| `cmd` | `str` | A command to be executed in this pane | yes |


#### `start_at` options

| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `window` | `str` | Name of the window to have active on attach | conditional yes; if `pane` is present |
| `pane` | `int` | Index of the pane to have active on attach | conditional yes; if `window` is present |


#### Example session config
```yaml
name: example_session
workdir: path/to/work/dir

windows:
  - name: first_window
    panes:
      - vertical: 50
        cmd: echo "First pane!"
      - horizontal: 30
        cmd: echo "Second pane!"
      - vertical: 10
        cmd: echo "Third pane!"
    cmd: echo "First window!"
  - name: second_window
    panes:
      - horizontal: 50
      - vertical: 50
    cmd: echo "Second window!"

start_at:
  window: first_window
  pane: 0
```

### Workspace config

> [!NOTE]
> Your workspace configuration should be in `~/.config/automux/workspace/`. See `automux --help` for more info.


| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `name` | `str` | Name of the tmux workspace | no |
| `sessions` | `list(dict)` | A list of session objects (see [Session config](#session-config)) | no |


#### Example workspace config
```yaml
name: example_workspace

sessions:
  - name: main_session
    workdir: path/to/work/dir
    windows:
      - name: first_window
        panes:
          - vertical: 50
            cmd: echo "First pane!"
          - horizontal: 30
            cmd: echo "Second pane!"
          - vertical: 10
            cmd: echo "Third pane!"
        cmd: echo "First window!"
      - name: second_window
        panes:
          - horizontal: 50
          - vertical: 50
        cmd: echo "Second window!"
    start_at:
      window: first_window
      pane: 0

  - name: helper_session
    workdir: path/to/work/dir
    windows:
      - name: helper_first_window
        panes:
          - vertical: 50
            cmd: echo "First pane 123!"
          - horizontal: 30
            cmd: echo "Second pane 123!"
          - vertical: 10
            cmd: echo "Third pane 123!"
        cmd: echo "First window 123!"
      - name: helper_second_window
        panes:
          - horizontal: 50
          - vertical: 50
        cmd: echo "Second window 123!"
    start_at:
      window: helper_first_window
      pane: 0
```

## Development
See [requirements](#requirements) first.

### Running
#### Using example config
To run this on the example using the [example config](.tmux/session.yml):
```shell
python src/main.py
```

##### Result
Help will be printed out as shown in [How to use](#how-to-use).

### Makefile
This project uses `Makefile` to `format` the code and do `lint` and `sanity` checks.

To use the `Makefile`, simply use `make` to display all available targets.

```console
$ make
help                           Prints help for targets with comments
format                         Format using ruff
lint                           Lint using mypy and ruff
sanity                         Sanity check before formatting
build                          Build automux binary
```
