# Automux - tmux config for each project
**NOTE**: This is still a work in progress, so not all features will work properly.

## Development
### Requirements
1. tmux 3.4
2. python 3.12
3. environment:
```shell
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running
#### Using example config
To run this on the example using the [example config](.tmux/session.yml):
```shell
python main.py
```

##### Result
As a result, you should be attached to a session named `MySession`, have two windows (`first_window`, `second_window`, and on both you should see an executed `echo` command)

### Makefile
This project uses `Makefile` to `format` the code and do `lint` and `sanity` checks.

To use the `Makefile`, simply use `make` to display all available targets.

```console
$ make
help                           Prints help for targets with comments
format                         Format using ruff
lint                           Lint using mypy and ruff
sanity                         Sanity check before formatting
```


### TODO:
- [ ] make the config per-project: each project should have a .tmux/session.yml to automatically create a session
- [x] add panes support: user should be able to add an N amount of panes horizontally or vertically in each window
- [x] default focus: which window and/or pane the user should have a focus on when the session is created and attached


## How to use
### Config
The config should be present in your project's root in `.tmux/session.yml` (this statement is _not yet implemented_).

#### Example config
```yaml
name: MySession

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


| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `name` | `str` | Name of the session | no |
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
