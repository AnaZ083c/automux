from subprocess import CalledProcessError, check_output, DEVNULL


class Tmux:
    @classmethod
    def get_version(cls) -> str:
        try:
            result = check_output(["tmux", "-V"], stderr=DEVNULL, text=True)
            return result
        except CalledProcessError:
            raise
