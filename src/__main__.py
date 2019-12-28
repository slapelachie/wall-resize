import argparse
import sys

from resizer import resizer

#TODO: Add proper logging
#TODO: Comment everything
#TODO: Allow for custom sizes in arguments

def get_args():
	arg = argparse.ArgumentParser(description="Resize pictures")

	arg.add_argument('-i', metavar='/path/to/file',
		help="Input file")

	arg.add_argument('-m', action="store_true",
		help="Move old files once scaled")

	arg.add_argument('-w', action="store_true",
		help="Use waifu scaling on smaller images (This process takes a long time)")

	return arg

def parse_args(parser):
	args = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		sys.exit(1)

	if args.i:
		resizer.resize(args.i, args.m, args.w, 1920, 1080)
		pass

def main():
	parser = get_args()
	parse_args(parser)
	pass

if(__name__ == "__main__"):
	main()