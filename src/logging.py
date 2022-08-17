import pathlib
import datetime


class Logger:
    def __init__(self, file):
        self._file = pathlib.Path(file)

    def log_item(self, filename, error):
        with open(self._file, "a") as f:
            f.write(f"{datetime.datetime.utcnow()}\t{filename}\t{error}\n")
