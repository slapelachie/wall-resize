import logging
import tqdm

# The default format used for logging
default_format = "[%(levelname)s] %(message)s\n"
bar_format = "{percentage:3.0f}% {n}/{total}"


class defaultLoggingHandler(logging.StreamHandler):
    """ The default logging handler """

    def emit(self, record):
        try:
            self.setFormatter(logging.Formatter(default_format))
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class tqdmLoggingHandler(logging.Handler):
    """ Logger used in compatibilty with tqdm """

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            self.setFormatter(logging.Formatter(default_format))
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def setup_logger(name, level, handler):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# Change the names of the logger level
logging.addLevelName(logging.CRITICAL, "C")
logging.addLevelName(logging.ERROR, "E")
logging.addLevelName(logging.WARNING, "W")
logging.addLevelName(logging.INFO, "I")
logging.addLevelName(logging.DEBUG, "D")
