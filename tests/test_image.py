import unittest
from unittest.mock import patch

from twissify.image import load_image_url, open_image_binary


class TestImage(unittest.TestCase):
    @patch("twissify.image.open_image_binary",
           **{"return_value": "ImageFile"})
    @patch("requests.get", **{"return_value.content": "bytes"})
    def test_load_image_url(self, requests_get, open_image_binary):
        url = "url"
        expectations = [(None, 199),
                        ("ImageFile", 200),
                        (None, 201)]
        expectation_requests_get = url
        expectation_oib = "bytes"

        for expectation in expectations:
            requests_get.return_value.status_code = expectation[1]
            image, status_code = load_image_url(url)
            requests_get.assert_called_with(expectation_requests_get)
            self.assertEqual(expectation[0], image)
            self.assertEqual(expectation[1], status_code)
            if open_image_binary.called:
                open_image_binary.assert_called_once_with(expectation_oib)

    @patch("PIL.Image.open", return_value="Success!")
    @patch("io.BytesIO", return_value="bytes")
    def test_open_image_binary(self, io_BytesIO, Image_open):
        string = "test"
        expectation = "Success!"
        expectation_io_BytesIO = string
        expectation_Image_open = "bytes"
        actual = open_image_binary(string)
        io_BytesIO.assert_called_once_with(expectation_io_BytesIO)
        Image_open.assert_called_once_with(expectation_Image_open)
        self.assertEqual(expectation, actual)


if __name__ == "__main__":
    unittest.main()
