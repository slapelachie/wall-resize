import os
import sys
import subprocess
import logging
import tqdm
import shutil
import re

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
    def __init__(self, image_path, out_directory, dimensions):
        self.image_path = image_path
        # self.out_directory = out_directory
        self.dimensions = dimensions
        self.move_old_file = False
        self.use_waifu = False
        self.verbose_logging = False
        self.images = []
        self.out_directory = None

        if os.path.isfile(self.image_path):
            self.images = [utils.get_image(self.image_path)]
            self.out_directory = os.path.abspath(os.path.dirname(self.image_path))
        elif os.path.isdir(self.image_path):
            self.images = utils.get_dir_imgs(self.image_path)
            self.out_directory = os.path.abspath(self.image_path)
        else:
            print("Passed file is not directory or file. Exiting...")
            exit(1)

    def set_use_waifu(self, use_waifu):
        self.use_waifu = use_waifu

    def set_move_old_file(self, move_old_file):
        self.move_old_file = move_old_file

    def set_verbose_logging(self, verbose_logging):
        self.verbose_logging = verbose_logging

    def _create_needed_directories(self, out_path, old_directory, waifu_directory):
        os.makedirs(out_path, exist_ok=True)

        if self.move_old_file:
            os.makedirs(old_directory, exist_ok=True)

        if self.use_waifu:
            os.makedirs(waifu_directory, exist_ok=True)

    def resize_image(self):
        nwidth, nheight = self.dimensions

        out_path = os.path.join(
            self.out_directory, "rescaled_{}x{}".format(nwidth, nheight)
        )
        old_directory = os.path.join(self.out_directory, "before-rescale/")
        waifu_directory = os.path.join(self.out_directory, "waifu/")

        self._create_needed_directories(out_path, old_directory, waifu_directory)

        for i in tqdm.tqdm(range(len(self.images))):
            image_path = utils.get_image(os.path.join(self.image_path, self.images[i]))
            original_image_path = image_path
            image_out_path = os.path.join(out_path, os.path.basename(image_path))

            if os.path.isfile(image_out_path):
                continue
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
            except:
                print("Cannot get image info for {}. Skipping...".format(image_path))
                continue

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
                else:
                    waifu_image_out_path = os.path.join(
                        waifu_directory, os.path.basename(image_path)
                    )

                    scale_size = max([round(nwidth / width), round(height / nheight)])
                    print("running")

                    subprocess.run(
                        [
                            "waifu2x-converter-cpp",
                            "-m",
                            "noise-scale",
                            "--noise-level",
                            "1",
                            "--scale-ratio",
                            str(scale_size),
                            "-i",
                            image_path,
                            "-o",
                            waifu_image_out_path,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                    )
                    print("finish running")
                    image_path = waifu_image_out_path
                    try:
                        with Image.open(image_path) as img:
                            width, height = img.size
                    except:
                        sys.exit(1)

            # Gets the resize size while keeping the aspect ratio the same
            ratio = min(width / nwidth, height / nheight)
            rwidth = int(width / ratio)
            rheight = int(height / ratio)

            # Crop to the middle using the passed width and height
            crop_box = (
                (rwidth - nwidth) / 2,
                (rheight - nheight) / 2,
                (rwidth + nwidth) / 2,
                (rheight + nheight) / 2,
            )

            try:
                with Image.open(image_path) as img:
                    # tqdm_log.info("Descaling image %s", image)
                    # Resizes the image keeping the aspect ratio
                    img = img.resize((rwidth, rheight), Image.LANCZOS)
                    # Crop the image to match the dimensions passed
                    img = img.crop(crop_box)
                    img.save(image_out_path)
                    # tqdm_log.info("Saved new image to %s", image_path)
            except:
                raise

            if self.move_old_file:
                # tqdm_log.info("Moving old image %s to %s", image_path, old_directory)
                shutil.move(original_image_path, old_directory)


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