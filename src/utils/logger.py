import logging
import tqdm

default_format = ("[%(levelname)s\033[0m] "
	"\033[1;31m%(module)s\033[0m: "
	"%(message)s")

class defaultLoggingHandler(logging.StreamHandler):
	def emit(self, record):
		try:
			self.setFormatter(logging.Formatter(default_format+'\n'))
			msg = self.format(record)
			stream = self.stream
			stream.write(msg)
			self.flush()
		except(KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

class tqdmLoggingHandler(logging.Handler):
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

logging.addLevelName(logging.CRITICAL, 'C')
logging.addLevelName(logging.ERROR, 'E')
logging.addLevelName(logging.WARNING, 'W')
logging.addLevelName(logging.INFO, 'I')
logging.addLevelName(logging.DEBUG, 'D')