import os
from logging.config import fileConfig
from logging import getLogger
from module import PDFtoTIFFConverter

# popplerのバイナリにpathを通す
os.environ["PATH"] += f":{os.path.dirname(os.path.abspath(__file__))}/poppler/"
os.environ["LD_LIBRARY_PATH"] += f":{os.path.dirname(os.path.abspath(__file__))}/poppler/"

# logger設定
logger = getLogger(__name__)
fileConfig("./config/logging.conf", disable_existing_loggers=False)


def handler(event, context):
    pdf_to_tiff_converter = PDFtoTIFFConverter()
    result = pdf_to_tiff_converter.execution(event, context)
    return result
