import unittest
import re
from wall_resize.utils import utils


class TestUtils(unittest.TestCase):
    def test_get_image(self):
        utils.get_image("tests/assets/test_dir/test.jpg")

    def test_get_dir_images(self):
        images = utils.get_dir_imgs("tests/assets/test_dir")
        self.assertTrue(len(images) == 1)
        self.assertTrue(images == ["test.jpg"])

    def test_get_images_file(self):
        images = utils.get_images("tests/assets/test_dir/test.jpg")
        self.assertIn("test.jpg", images[0])

    def test_get_images_dir(self):
        images = utils.get_images("tests/assets/test_dir/")
        self.assertEqual(images, ["test.jpg"])

    def test_get_random_string(self):
        regex_match = r"\b[a-z]{6}\b"
        random_string = utils.get_random_string(6)
        regex = re.compile(regex_match)
        match = regex.match(random_string)

        self.assertIsNot(match, None)
