import os
from pdf2image import convert_from_bytes
os.environ["PATH"] = os.environ.get("PATH", "") + ":/var/task/poppler/"
os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + ":/var/task/poppler/"


def handler(event, context):
    input_path = "data/tis_200206.pdf"
    output_path = "/tmp/data/test.tif"
    if not os.path.exists("/tmp/data/"):
        os.makedirs("/tmp/data/")

    with open(input_path, "rb") as f:
        images = convert_from_bytes(
            pdf_file=f.read(),
            grayscale=True)
    images[0].save(
        output_path,
        format='TIFF',
        dpi=(400, 400),
        compression="tiff_deflate",
        save_all=True,
        append_images=images[1:])

    with open(output_path, "rb") as f:
        return f.read()
