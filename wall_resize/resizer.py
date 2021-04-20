import os
import sys
import subprocess
import logging
import tqdm
import shutil
import re
from PIL import Image
from typing import Tuple, Dict, List

from .utils import utils, logger

# Setup the required loggers
log = logger.setup_logger(
    __name__ + ".default", logging.WARNING, logger.defaultLoggingHandler()
)
tqdm_log = logger.setup_logger(
    __name__ + ".tqdm", logging.WARNING, logger.tqdmLoggingHandler()
)


class Resizer:
    def __init__(
        self,
        image_path,
        dimensions,
        out_directory=None,
        use_waifu=False,
        replace_image=False,
        verbose_logging=False,
        progress=False,
    ):
        self.image_path = image_path
        self.out_directory = out_directory
        self.dimensions = dimensions
        self.replace_image = replace_image
        self.use_waifu = use_waifu
        self.verbose_logging = verbose_logging
        self.progress = progress
        self.images = []

        self.images = utils.get_images(self.image_path)
        if not self.images:
            log.critical("Passed file is not directory or file. Exiting...")
            exit(1)

        if not self.out_directory:
            self.out_directory = utils.get_path_file_folder(self.image_path)

        if verbose_logging:
            log.setLevel(logging.INFO)
            tqdm_log.setLevel(logging.INFO)

    def resize_images(self) -> None:
        nwidth, nheight = self.dimensions

        out_path = os.path.join(
            self.out_directory, "rescaled_{}x{}".format(nwidth, nheight)
        )
        os.makedirs(out_path, exist_ok=True)

        for i in tqdm.tqdm(
            range(len(self.images)),
            bar_format=logger.bar_format,
            disable=not self.progress,
        ):
            image_path = utils.get_image(os.path.join(self.image_path, self.images[i]))
            image_out_path = os.path.join(
                out_path,
                "{}.png".format(os.path.splitext(os.path.basename(image_path))[0]),
            )

            # Check if the file already exists
            if os.path.isfile(image_out_path):
                continue

            image = resize_image(image_path, (nwidth, nheight), self.use_waifu)
            if not image:
                continue

            try:
                image.save(image_out_path)
            except:
                raise

            if self.replace_image:
                os.remove(image_path)
                shutil.move(
                    image_out_path, "{}.png".format(os.path.splitext(image_path)[0])
                )

        if self.replace_image:
            try:
                os.rmdir(out_path)
            except:
                log.warn("{} contains files. Not removing directory".format(out_path))
                pass


def get_ratio_dimensions(
    dimensions: Tuple[int, int], new_dimensions: Tuple[int, int]
) -> Tuple[int, int]:
    # Gets the resize size while keeping the aspect ratio the same
    width, height = dimensions
    new_width, new_height = new_dimensions

    ratio = min(width / new_width, height / new_height)
    rwidth = int(width / ratio)
    rheight = int(height / ratio)

    return (rwidth, rheight)


def get_dimensions_from_string(dimensions: str) -> Tuple[int, int]:
    # Finds images matching 0-9x-09
    dimension_regex = r"([\d]+)(?:[xX])([\d]+)"
    regex = re.compile(dimension_regex)

    match = regex.match(str(dimensions))
    if match == None:
        log.critical("Could not find valid dimensions! Exiting...")
        sys.exit(1)

    width = match.group(1)
    height = match.group(2)

    return (int(width), int(height))


def upscale_image(image_path: str, scale_factor: float) -> Image:
    out_path = "/tmp/wall-resize-{}.png".format(utils.get_random_string(6))

    subprocess.run(
        [
            "waifu2x-converter-cpp",
            "-i",
            image_path,
            "-m",
            "noise-scale",
            "--noise-level",
            "1",
            "--scale-ratio",
            str(scale_factor),
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


def resize_image(
    image_path: str, new_dimensions: Tuple[int, int], use_waifu: bool
) -> Image:
    new_width, new_height = new_dimensions
    image = None

    try:
        image = Image.open(image_path)
    except:
        log.error("Cannot get image info for {}. Skipping...".format(image_path))
        return None

    width, height = image.size

    if (width == new_width) and (height == new_height):
        return None
    elif (width < new_width) or (height < new_height):
        if not use_waifu:
            tqdm_log.warn(
                "Image {} is smaller than specified dimensions. Skipping...".format(
                    image_path
                )
            )
            return None

        scale_factor = max([round(new_width / width, 2), round(new_height / height, 2)])
        image = upscale_image(image_path, scale_factor)
        width, height = image.size

    rwidth, rheight = get_ratio_dimensions((width, height), (new_width, new_height))

    # Crop to the middle using the passed width and height
    crop_box = (
        (rwidth - new_width) / 2,
        (rheight - new_height) / 2,
        (rwidth + new_width) / 2,
        (rheight + new_height) / 2,
    )

    image = image.resize((rwidth, rheight), Image.LANCZOS)
    image = image.crop(crop_box)

    return image