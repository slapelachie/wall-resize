import argparse
import sys
import logging

from . import resizer
from .utils import logger

log = logger.setup_logger(__name__, logging.WARNING, logger.defaultLoggingHandler())


def get_args():
    arg = argparse.ArgumentParser(description="Resize pictures")

    arg.add_argument("-i", metavar="/path/to/file", help="Input file")

    arg.add_argument("-o", metavar="/path/to/file", help="Output directory")

    arg.add_argument(
        "-d",
        metavar="WIDTHxHEIGHT",
        help="Dimensions of rescaled image. Default: 1920x1080",
    )

    arg.add_argument("-v", action="store_true", help="Verbose logging")

    arg.add_argument("-m", action="store_true", help="Move old files once scaled")

    arg.add_argument(
        "-w",
        action="store_true",
        help="Use waifu scaling on smaller images (This process takes a long time)",
    )

    return arg


def parse_args(parser):
    args = parser.parse_args()

    DIMENSIONS = (1920, 1080)

    # If the amount of parsed arguments are less then 1, print the help
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.d:
        DIMENSIONS = resizer.get_dimensions_from_string(args.d)

    if args.i:
        resizer_engine = resizer.Resizer(args.i, args.o, DIMENSIONS)
        resizer_engine.set_move_old_file(args.m)
        resizer_engine.set_use_waifu(args.w)
        resizer_engine.set_verbose_logging(args.v)
        resizer_engine.resize_image()
    else:
        log.warning("Argument -i needs to be specified.")
        parser.print_help()
        sys.exit(1)


def main():
    parser = get_args()
    parse_args(parser)


if __name__ == "__main__":
    main()
