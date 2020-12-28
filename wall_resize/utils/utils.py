import os
import logging
import string
import random

from . import logger

# Setup the logger
log = logger.setup_logger(__name__, logging.WARNING, logger.defaultLoggingHandler())


def get_image(image_path):
    if os.path.isfile(image_path):
        log.debug("Found image %s", image_path)
        return os.path.abspath(image_path)
    else:
        log.critical("Unable to find image %s", image_path)
        raise Exception("Image not found at {}".format(image_path))


def get_dir_imgs(image_directory):
    file_types = ("png", "jpg", "jpeg")
    return [
        img.name
        for img in os.scandir(image_directory)
        if img.name.lower().endswith(file_types)
    ]


def get_images(image_path):
    if os.path.isfile(image_path):
        return [get_image(image_path)]
    elif os.path.isdir(image_path):
        return get_dir_imgs(image_path)
    else:
        return None


def get_path_file_folder(path):
    if os.path.isfile(path):
        return os.path.abspath(os.path.dirname(path))
    elif os.path.isdir(path):
        return os.path.abspath(path)
    else:
        return None


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
