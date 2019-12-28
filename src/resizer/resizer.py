import os
import sys
import subprocess

from utils import utils
from PIL import Image

def resize(file, old_move, nwidth, nheight):
	images = None
	if os.path.isfile(file):
		images = [utils.get_image(file)]
	elif os.path.isdir(file):
		images = utils.get_dir_imgs(file)
	else:
		print("not file")
		sys.exit(1)

	for image in images:
		output_path = os.path.join(os.path.dirname(file), 'rescaled_' + str(nwidth) + "-" + str(nheight))
		image = utils.get_image(os.path.join(file, image))
		old_dir = os.path.join(os.path.dirname(image), "before-rescale/")
		os.makedirs(output_path, exist_ok=True)

		if old_move:
			os.makedirs(old_dir, exist_ok=True)

		image_path = os.path.join(output_path, os.path.basename(image))

		if os.path.isfile(image_path):
			print("File " + image_path + " already exists. Skipping...")
			continue

		try:
			with Image.open(image) as img:
				width, height = img.size
		except:
			print("Could not get image info for ", image)
			sys.exit(1)

		if (width < nwidth) or (height < nheight):
			print("Image " + image + " is smaller then specified dimensions. Skipping...")
			continue
		elif (width == nwidth) or (height == nheight):
			print("Image " + image + " has the same dimensions as specified. Skipping...")
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
		except:
			raise
			sys.exit(1)
		
		if old_move:
			subprocess.run(["mv", image, old_dir])