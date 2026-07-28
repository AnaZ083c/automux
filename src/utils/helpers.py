class Logger:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def info(self, msg: str) -> None:
        print(msg)

    def debug(self, msg: str) -> None:
        if self.verbose:
            print(f"Debug: {msg}")

    def error(self, msg: str) -> None:
        print(f"Error: {msg}")
