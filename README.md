# TMUX config for each project
**NOTE**: This is still a work in progress, so not all features will work properly.

## Requirements
1. tmux 3.4
2. python 3.12
3. environment:
```shell
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running
### Using example config
To run this on the example using the [example config](.tmux/session.yml):
```shell
python main.py
```

#### Result
As a result, you should be attached to a session named `MySession`, have two windows (`first_window`, `second_window`, and on both you should see an executed `echo` command)


## Config
The config should be present in your project's root in `.tmux/session.yml` (this statement is _not yet implemented_).

### Example config
```yaml
name: MySession

windows:
  - name: first_window
    cmd: echo "First window!"
  - name: second_window
    cmd: echo "Second window!
```


| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `name` | `str` | Name of the session | no |
| `windows` | `list(dict)` | List of windows to be created in the session | yes |


### `windows` options

| Config | Type | Description | Optional |
| --------------- | --------------- | --------------- | --------------- |
| `name` | `str` | Name of the window in a session | no |
| `cmd` | `str` | A command to be executed in this window | yes |


## TODO:
- [ ] make the config per-project: each project should have a .tmux/session.yml to automatically create a session
- [ ] add panes support: user should be able to add an N amount of panes horizontally or vertically in each window
- [ ] default focus: which window and/or pane the user should have a focus on when the session is created and attached

