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

    arg.add_argument(
        "-w",
        action="store_true",
        help="Use waifu scaling on smaller images (This process takes a long time)",
    )

    arg.add_argument(
        "--replace", action="store_true", help="replace the file once scaled"
    )

    arg.add_argument(
        "--progress", action="store_true", help="Display progress of resizing files"
    )

    return arg


def parse_args(parser):
    args = parser.parse_args()

    dimensions = (1920, 1080)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.d:
        dimensions = resizer.get_dimensions_from_string(args.d)

    if args.i:
        resizer_engine = resizer.Resizer(
            args.i,
            dimensions,
            out_directory=args.o,
            replace_image=args.replace,
            use_waifu=args.w,
            verbose_logging=args.v,
            progress=args.progress,
        )
        resizer_engine.resize_images()
    else:
        log.warning("Argument -i needs to be specified.")
        parser.print_help()
        sys.exit(1)


def main():
    parser = get_args()
    parse_args(parser)


if __name__ == "__main__":
    main()
