import argparse
import sys
import logging
import re

from resizer import resizer
from utils import logger

#Finds images matching 0-9x-09
dimension_regex = r'([\d]+)(?:[xX])([\d]+)'
regex = re.compile(dimension_regex)

# Setup the logger
log = logger.setup_logger(__name__, logging.WARNING, logger.defaultLoggingHandler())

def get_args():
	"""List of all arguments supported"""

	arg = argparse.ArgumentParser(description="Resize pictures")

	arg.add_argument('-i', metavar='/path/to/file',
		help="Input file")

	arg.add_argument('-o', metavar="/path/to/file",
		help='Output directory')

	arg.add_argument('-d', metavar='WIDTHxHEIGHT',
		help="Dimensions of rescaled image. Default: 1920x1080")	

	arg.add_argument('-v', action="store_true",
		help="Verbose logging")

	arg.add_argument('-m', action="store_true",
		help="Move old files once scaled")

	arg.add_argument('-w', action="store_true",
		help="Use waifu scaling on smaller images (This process takes a long time)")

	return arg

def parse_args(parser):
	"""
	Parses arguments specified by the parser
	
	Arguments:
		parser (idk): The parser to be used
	"""
	args = parser.parse_args()

	# Defaults	
	DIMENSIONS = (1920, 1080)

	# If the amount of parsed arguments are less then 1, print the help
	if len(sys.argv) <= 1:
		parser.print_help()
		sys.exit(1)

	# If the dimension argument has been passed
	if args.d:
		# Match the regex with the passed dimension string
		match = regex.match(str(args.d))
		if match == None:
			log.critical("Could not find valid dimensions! Exiting...")
			sys.exit(1)
		log.debug("Matched regex \"%s\" to \"%s\" resulting in \"%s\"", dimension_regex, str(args.d), match.group(0))

		# Set the dimensions of the new image
		width = match.group(1)
		height = match.group(2)
		DIMENSIONS = (int(width), int(height))

	# If the image argument has been passed
	# This is required and the program will not work without it
	if args.i:
		resizer.resize(args.i, args.o, args.m, args.w, args.v, DIMENSIONS)
	else:
		log.warning("Argument -i needs to be specified.")
		parser.print_help()
		sys.exit(1)

def main():
	parser = get_args()
	parse_args(parser)

if(__name__ == "__main__"):
	main()