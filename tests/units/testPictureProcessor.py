import unittest
from unittest.mock import MagicMock, patch
import src.PictureProcessor as PictureProcessor


class TestPictureProcessor(unittest.TestCase):
    def setUp(self):
        self.session_options = {
            'root_directory_object': '/path/to/root/directory',
            'new_directory_object': '/path/to/new/directory'
        }

        # Mock PIL.Image.open method
        self.mock_open = MagicMock()
        self.mock_pil_image = MagicMock()
        self.mock_open.return_value = self.mock_pil_image

        # Patch PIL.Image.open with the mock
        self.patcher = patch('picture_processor.PIL.Image.open', self.mock_open)
        self.patcher.start()

        self.processor = PictureProcessor(self.session_options)

    def tearDown(self):
        self.patcher.stop()

    def test__compile_pic_list(self):
        # Initialize PictureProcessor instance
        processor = PictureProcessor(self.session_options)

        # Mock glob return value
        processor._rootDirectoryPath.glob = MagicMock(return_value=['file1.jpg', 'file2.png'])

        # Call _compile_pic_list method
        pic_list = processor._compile_pic_list()

        # Assert that the expected file extensions are included in the pic list
        self.assertIn('file1.jpg', pic_list)
        self.assertIn('file2.png', pic_list)

    def test__hash_pic(self):
        # Call _hash_pic method with a mock file path
        pic_hash = self.processor._hash_pic('/path/to/pic.jpg')

        # Assert that the mock hasher update and hexdigest methods were called
        self.mock_hasher = MagicMock()
        self.mock_hasher.update.assert_called()
        self.mock_hasher.hexdigest.assert_called()

    def test__organize_pic_by_time(self):
        # Mock PIL.Image.getexif method return value
        self.mock_pil_image.getexif.return_value = {306: '2022:03:20 12:30:45'}

        # Call _organize_pic_by_time method with mock arguments
        copy_location = self.processor._organize_pic_by_time(self.mock_pil_image, 'pic.jpg')

        # Assert that the copy location is as expected
        expected_location = '/path/to/new/directory/2022/03/pic.jpg'
        self.assertEqual(copy_location, expected_location)


if __name__ == '__main__':
    unittest.main()
