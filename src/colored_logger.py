"""
A simple module allowing colored log messages
"""
import logging


class ColoredLoggerAdapter(logging.LoggerAdapter):
    """
    A simple class allowing colored log messages
    """
    black, red, green, yellow, blue, magenta, cyan, white = ["\033[1;{:d}m".format(30 + x) for x in range(8)]
    reset_seq = "\033[0m"
    bold_seq = "\033[1m"

    def __init__(self, logger, extra=None):
        super(ColoredLoggerAdapter, self).__init__(logger, extra)

    def info(self, msg, *args, **kwargs):
        super(ColoredLoggerAdapter, self).info(self.blue + msg + self.reset_seq)

    def debug(self, msg, *args, **kwargs):
        super(ColoredLoggerAdapter, self).debug(self.green + msg + self.reset_seq)

    def warning(self, msg, *args, **kwargs):
        super(ColoredLoggerAdapter, self).warning(self.cyan + msg + self.reset_seq)

    def error(self, msg, *args, **kwargs):
        super(ColoredLoggerAdapter, self).error(self.red + msg + self.reset_seq)