import os
import sys
import subprocess
import logging
import tqdm

from utils import utils, logger
from PIL import Image

# Setup the required loggers
log = logger.setup_logger(__name__+'.default', logging.WARNING, logger.defaultLoggingHandler())
tqdm_log = logger.setup_logger(__name__+'.tqdm', logging.WARNING, logger.tqdmLoggingHandler())

FNULL = open(os.devnull, 'w')

def resize(file, output_arg, old_move, use_waifu, verbose, dimensions):
	"""
	Used to resize the image to a specific size, the way the arguments are parsed
	here are terribly done and will need to be improved in the future

	FIXME: this

	Arguments:
		file (string): The path to the file
		output_arg (string): The path to the output directory
		old_move (boolean): If the used image should be moved out of the directory
		use_waifu (boolean): If images smaller then the specified dimensions should be upscaled
		verbose (boolean): If verbose logging should be enabled (log level of INFO)
		dimensions (tuple[int]): The dimensions to be used to resize the image
	"""

	# If the verbose option has been passed, set log level to INFO
	if verbose:
		log.setLevel(logging.INFO)
		tqdm_log.setLevel(logging.INFO)

	nwidth, nheight = dimensions
	log.debug("Using dimensions: %sx%s", nwidth, nheight)

	# Check if the file is a file or a dir
	if os.path.isfile(file):
		images = [utils.get_image(file)]
	elif os.path.isdir(file):
		images = utils.get_dir_imgs(file)
	else:
		log.critical("%s is not a file! Exiting...", file)
		sys.exit(1)
	
	output_dir = os.path.abspath(os.path.dirname(file))

	# If the output argument has been passed, set it to that
	if output_arg:
		if(os.path.isdir(output_arg)):
			output_dir = os.path.abspath(output_arg)
		else:
			log.error("Specified output directory %s is not a path, using image path %s instead...",
				output_arg, output_dir)
		
	# Assign directories
	output_path = os.path.join(output_dir, 'rescaled_' + str(nwidth) + "-" + str(nheight))
	old_dir = os.path.join(output_dir, "before-rescale/")
	waifu_dir = os.path.join(output_dir, "waifu/")

	# Create the output path directory
	log.debug("Attempting to create directory %s", output_path)
	os.makedirs(output_path, exist_ok=True)
	log.info("Outputing all images to %s", output_path)

	if use_waifu:
		log.debug("Attempting to create directory %s", waifu_dir)
		os.makedirs(waifu_dir, exist_ok=True)
		log.info("Storing all images scaled with waifu2x in %s", waifu_dir)

	if old_move:
		log.debug("Attempting to create directory %s", old_dir)
		os.makedirs(old_dir, exist_ok=True)
		log.info("Moving all used images to %s", old_dir)

	"""
	Loops through every image given
	tqdm adds a progress bar to the bottom of the output

	WARNING: Use tqdm_log when logging in this loop or it will
	break the progress bar
	"""
	for i in tqdm.tqdm(range(len(images))):
		image = utils.get_image(os.path.join(file, images[i]))
		original_img_path = image		
		image_path = os.path.join(output_path, os.path.basename(image))

		if os.path.isfile(image_path):
			tqdm_log.info("File %s already exists. Skipping...", image_path)
			continue

		# Try to get the dimensions of the passed image
		try:
			with Image.open(image) as img:
				width, height = img.size
		except:
			tqdm_log.critical("Could not get image info for %s", image)
			sys.exit(1)

		# Check if the image width is less then the passed width
		# Applies to height as well
		if (width < nwidth) or (height < nheight):
			if not use_waifu:
				tqdm_log.info("Image %s is smaller then specified dimensions. Skipping...", image)
				tqdm_log.info("If you wish to upscale this image, run this command again using the -w option")
				continue
			else:
				tqdm_log.info("Upscaling image %s using waifu2x...", image)
				while (width < nwidth) or (height < nheight):
					waifu_image = os.path.join(waifu_dir, os.path.basename(image))
					subprocess.run(['waifu2x-converter-cpp', '-m', 'noise-scale', '--noise-level', '1', '-i', image, '-o', waifu_image], 
						stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					image = waifu_image
					try:
						with Image.open(image) as img:
							width, height = img.size
					except:
						tqdm_log.info("Could not get image info for %s", image)
						sys.exit(1)

		# Check if the image width is the same as the passed width
		# Applies to height as well
		elif (width == nwidth) or (height == nheight):
			tqdm_log.info("Image %s has the same dimensions as specified. Skipping...")
			continue	

		# Gets the resize size while keeping the aspect ratio the same
		ratio = min(width/nwidth, height/nheight)
		rwidth = int(width/ratio)
		rheight = int(height/ratio)

		# Crop to the middle using the passed width and height
		crop_box = (
			(rwidth-nwidth)/2,
			(rheight-nheight)/2,
			(rwidth+nwidth)/2,
			(rheight+nheight)/2
		)

		try:
			with Image.open(image) as img:
				# Resizes the image keeping the aspect ratio
				img = img.resize((rwidth, rheight), Image.LANCZOS)
				# Crop the image to match the dimensions passed
				img = img.crop(crop_box)
				img.save(image_path)
				tqdm_log.info("Saved new image to %s", image_path)
		except:
			raise
		
		if old_move:
			tqdm_log.info("Moving old image %s to %s", original_img_path, old_dir)
			subprocess.run(["mv", original_img_path, old_dir])