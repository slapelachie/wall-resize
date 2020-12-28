import os
import sys
import subprocess
import logging
import tqdm
import shutil
import re
import string
import random

from .utils import utils, logger
from PIL import Image

# Setup the required loggers
log = logger.setup_logger(
    __name__ + ".default", logging.WARNING, logger.defaultLoggingHandler()
)
tqdm_log = logger.setup_logger(
    __name__ + ".tqdm", logging.WARNING, logger.tqdmLoggingHandler()
)

FNULL = open(os.devnull, "w")


class Resizer:
    def __init__(
        self,
        image_path,
        dimensions,
        out_directory=None,
        use_waifu=False,
        replace_image=False,
        verbose_logging=False,
    ):
        self.image_path = image_path
        self.out_directory = out_directory
        self.dimensions = dimensions
        self.replace_image = replace_image
        self.use_waifu = use_waifu
        self.verbose_logging = verbose_logging
        self.images = []

        self.images = get_images(self.image_path)
        if not self.images:
            print("Passed file is not directory or file. Exiting...")
            exit(1)

        if not self.out_directory:
            self.out_directory = os.path.abspath(os.path.dirname(self.image_path))

    def resize_image(self):
        nwidth, nheight = self.dimensions

        out_path = os.path.join(
            self.out_directory, "rescaled_{}x{}".format(nwidth, nheight)
        )
        os.makedirs(out_path, exist_ok=True)

        for i in tqdm.tqdm(range(len(self.images))):
            image_path = utils.get_image(os.path.join(self.image_path, self.images[i]))
            image_out_path = os.path.join(out_path, os.path.basename(image_path))
            image = None

            if os.path.isfile(image_out_path):
                continue

            try:
                image = Image.open(image_path)
            except:
                print("Cannot get image info for {}. Skipping...".format(image_path))
                continue

            width, height = image.size

            if (width == nwidth) and (height == nheight):
                continue
            elif (width < nwidth) or (height < nheight):
                if not self.use_waifu:
                    print(
                        "Image {} is smaller than specified dimensions. Skipping...".format(
                            image_path
                        )
                    )
                    continue

                scale_factor = max([round(nwidth / width), round(height / nheight)])
                image = upscale_image(image_path, scale_factor)
                width, height = image.size

            rwidth, rheight = get_ratio_dimensions((width, height), (nwidth, nheight))

            # Crop to the middle using the passed width and height
            crop_box = (
                (rwidth - nwidth) / 2,
                (rheight - nheight) / 2,
                (rwidth + nwidth) / 2,
                (rheight + nheight) / 2,
            )

            try:
                image = image.resize((rwidth, rheight), Image.LANCZOS)
                image = image.crop(crop_box)
                image.save(image_out_path)
            except:
                raise

            if self.replace_image:
                shutil.move(image_out_path, image_path)

        if self.resize_image:
            try:
                os.rmdir(out_path)
            except:
                pass


def get_ratio_dimensions(dimensions, new_dimensions):
    # Gets the resize size while keeping the aspect ratio the same
    width, height = dimensions
    new_width, new_height = new_dimensions

    ratio = min(width / new_width, height / new_height)
    rwidth = int(width / ratio)
    rheight = int(height / ratio)

    return (rwidth, rheight)


def upscale_image(image_path, scale_factor):
    out_path = "/tmp/wall-resize-{}.png".format(get_random_string(6))

    subprocess.run(
        [
            "waifu2x-converter-cpp",
            "-m",
            "noise-scale",
            "--noise-level",
            "1",
            "--scale-ratio",
            str(scale_factor),
            "-i",
            image_path,
            "-o",
            out_path,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

    try:
        image = Image.open(out_path)
        os.remove(out_path)
        return image
    except:
        raise


def get_dimensions_from_string(dimension_string):
    # Finds images matching 0-9x-09
    dimension_regex = r"([\d]+)(?:[xX])([\d]+)"
    regex = re.compile(dimension_regex)

    match = regex.match(str(dimension_string))
    if match == None:
        # log.critical("Could not find valid dimensions! Exiting...")
        sys.exit(1)
    # log.debug(
    #    'Matched regex "%s" to "%s" resulting in "%s"',
    #    dimension_regex,
    #    str(dimension_string),
    #    match.group(0),
    # )

    width = match.group(1)
    height = match.group(2)

    return (int(width), int(height))


def get_images(image_path):
    if os.path.isfile(image_path):
        return [utils.get_image(image_path)]
    elif os.path.isdir(image_path):
        return utils.get_dir_imgs(image_path)
    else:
        return None


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
