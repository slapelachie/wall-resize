import os

def get_image(image):
	"""
	Get the absolute path of a passed file (image)

	Arguments:
		image (str) -- location of the file
	"""
	if os.path.isfile(image): 
		return os.path.abspath(image)

def get_dir_imgs(img_dir):
	"""
	Get a list of all images in a directory

	Arguments:
		img_dir (str) -- the directory where the images are stored
	"""
	file_types = ("png", "jpg", "jpeg")
	return [img.name for img in os.scandir(img_dir)
			if img.name.lower().endswith(file_types)]