import argparse
import sys

from resizer import resizer

def get_args():
	arg = argparse.ArgumentParser(description="Resize pictures")

	arg.add_argument('-i', metavar='/path/to/file',
		help="Input file")

	arg.add_argument('-m', action="store_true",
		help="Move old files once scaled")

	return arg

def parse_args(parser):
	args = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		sys.exit(1)

	if args.i:
		resizer.resize(args.i, args.m, 1920, 1080)
		pass

def main():
	parser = get_args()
	parse_args(parser)
	pass

if(__name__ == "__main__"):
	main()