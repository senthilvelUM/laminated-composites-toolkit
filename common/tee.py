"""File-like object that writes to multiple streams at once."""


class Tee:
    """Mirror write() calls to several file-like streams.

    Typical use: replace sys.stdout so every subsequent print()
    is echoed to a log file in addition to the terminal.

        sys.stdout = Tee(sys.stdout, open("log.txt", "w"))
    """

    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            stream.write(message)

    def flush(self):
        for stream in self.streams:
            stream.flush()
