import unittest
from wall_resize import resizer


class TestUtils(unittest.TestCase):
    def test_get_ratio_dimensions(self):
        ratio_dimensions = resizer.get_ratio_dimensions((2048, 1536), (1920, 1080))
        self.assertEqual(ratio_dimensions, (1920, 1440))

    def test_get_dimensions_from_string(self):
        dimensions = resizer.get_dimensions_from_string("1920x1080")
        self.assertEqual(dimensions, (1920, 1080))

    def test_resize_image(self):
        resized_image = resizer.resize_image(
            "tests/assets/test_dir/test.jpg", (50, 50), False
        )
        self.assertEqual(resized_image.size, (50, 50))
