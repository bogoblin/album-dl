from unittest import TestCase

from py_src.downloader import sanitize_path_segment


class Test(TestCase):
    def test_sanitize_path_segment(self):
        self.assertEqual(
            sanitize_path_segment("Are You Gonna Eat That?"),
            "Are You Gonna Eat That"
        )
