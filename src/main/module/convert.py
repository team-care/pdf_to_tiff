import os
from pdf2image import convert_from_path
from PIL import Image
from logging import getLogger
from .utils import LambdaRuntimeException


class PDFtoTIFFConverter:
    def __init__(self, dpi=400, compression="group4"):
        self._logger = getLogger(__name__)
        self._output_format = "TIFF"
        self._dpi = (dpi, dpi)
        self._compression = compression

    def convert(self, pdf_path, output_dir, filename):
        filepath = f"{output_dir}/{filename}.tif"
        try:
            # PDFからtifに変換
            image_path = convert_from_path(
                thread_count=5,
                pdf_path=pdf_path,
                output_folder=output_dir,
                output_file=filename,
                paths_only=True)
            # 白黒に変換
            images = [Image.open(image).convert("1") for image in image_path]
            # マルチページTIFFに変換して保存
            images[0].save(
                filepath,
                format=self._output_format,
                dpi=self._dpi,
                compression=self._compression,
                save_all=True,
                append_images=images[1:])
            # 余計なファイル削除
            for image in image_path:
                os.remove(image)
            self._logger.info(f"Convert success, save {filepath}")
            return filepath
        except Exception as ex:
            message = f"Failed convert {filename} to tiff"
            self._logger.error(message)
            self._logger.error(ex)
            raise LambdaRuntimeException(503, message)
