import os
import sys
import subprocess
import logging
import tqdm

from utils import utils, logger
from PIL import Image

log = logger.setup_logger(__name__+'.default', logging.WARNING, logger.defaultLoggingHandler())
tqdm_log = logger.setup_logger(__name__+'.tqdm', logging.WARNING, logger.tqdmLoggingHandler())

FNULL = open(os.devnull, 'w')

def resize(file, old_move, use_waifu, verbose, dimensions):

	if verbose:
		log.setLevel(logging.INFO)
		tqdm_log.setLevel(logging.INFO)

	nwidth, nheight = dimensions
	log.debug("Using dimensions: %sx%s", nwidth, nheight)

	if os.path.isfile(file):
		images = [utils.get_image(file)]
	elif os.path.isdir(file):
		images = utils.get_dir_imgs(file)
	else:
		log.critical("%s is not a file! Exiting...", file)
		sys.exit(1)
	
	output_path = os.path.join(os.path.dirname(file), 'rescaled_' + str(nwidth) + "-" + str(nheight))
	old_dir = os.path.join(os.path.dirname(file), "before-rescale/")
	waifu_dir = os.path.join(os.path.dirname(file), "waifu/")

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

	for i in tqdm.tqdm(range(len(images))):
		image = utils.get_image(os.path.join(file, images[i]))
		original_img_path = image		
		image_path = os.path.join(output_path, os.path.basename(image))

		if os.path.isfile(image_path):
			tqdm_log.info("File %s already exists. Skipping...", image_path)
			continue

		try:
			with Image.open(image) as img:
				width, height = img.size
		except:
			tqdm_log.critical("Could not get image info for %s", image)
			sys.exit(1)

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

		elif (width == nwidth) or (height == nheight):
			tqdm_log.info("Image %s has the same dimensions as specified. Skipping...")
			continue	

		ratio = min(width/nwidth, height/nheight)
		rwidth = int(width/ratio)
		rheight = int(height/ratio)

		crop_box = (
			(rwidth-nwidth)/2,
			(rheight-nheight)/2,
			(rwidth+nwidth)/2,
			(rheight+nheight)/2
		)

		try:
			with Image.open(image) as img:
				img = img.resize((rwidth, rheight), Image.LANCZOS)
				img = img.crop(crop_box)
				img.save(image_path)
				tqdm_log.info("Saved new image to %s", image_path)
		except:
			raise
		
		if old_move:
			tqdm_log.info("Moving old image %s to %s", original_img_path, old_dir)
			subprocess.run(["mv", original_img_path, old_dir])