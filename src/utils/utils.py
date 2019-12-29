import os
import logging

from utils import logger

# Setup the logger
log = logger.setup_logger(__name__, logging.WARNING, logger.defaultLoggingHandler())

def get_image(image):
	"""
	Get the absolute path of a passed file (image)

	Arguments:
		image (str) -- location of the file
	"""
	if os.path.isfile(image): 
		log.debug("Found image %s", image)
		return os.path.abspath(image)
	else:
		log.critical("Unable to find image %s, exiting...", image)

def get_dir_imgs(img_dir):
	"""
	Get a list of all images in a directory

	Arguments:
		img_dir (str) -- the directory where the images are stored
	"""
	file_types = ("png", "jpg", "jpeg")
	return [img.name for img in os.scandir(img_dir)
		if img.name.lower().endswith(file_types)]