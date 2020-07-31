import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../src/main"))
from module import PDFtoTIFFConverter


class TestConvert(unittest.TestCase):

    def test_convert(self):
        test_dir = os.path.join(os.path.dirname(__file__), "pdfs")
        pdf_path = os.path.join(test_dir, "S100IY60.pdf")
        converted_file_name = "converted"

        converter = PDFtoTIFFConverter()
        tiff_path = converter.convert(
            pdf_path=pdf_path,
            output_dir=test_dir,
            filename=converted_file_name)

        converted_path = os.path.join(test_dir, converted_file_name + ".tif")
        self.assertTrue(os.path.exists(converted_path))
        os.remove(converted_path)
