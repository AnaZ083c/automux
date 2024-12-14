from subprocess import run, CalledProcessError, check_output, Popen, PIPE, STDOUT, DEVNULL


class Tmux:
    @classmethod
    def get_version(cls) -> str:
        try:
            result = check_output(['tmux', '-V'], stderr=DEVNULL, text=True)
            return result
        except CalledProcessError:
            raise

