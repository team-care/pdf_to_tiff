from pathlib import Path
from pdf2image import convert_from_path


def convert(input_path, output_path=""):
    path = Path(input_path)
    if not path.exists():
        raise Exception(f"Input file {path} does not exist.")
    images = convert_from_path(str(path))
    if not output_path:
        output_path = path.with_suffix(".tif")
    else:
        output_path = Path(output_path)

    if not output_path.parent.exists():
        raise Exception(f"Output file location {output_path.parent} does not exist.")

    images = [i.convert("L") for i in images]  # to grayscale
    images[0].save(
        str(output_path),
        compression="tiff_deflate",
        save_all=True,
        append_images=images[1:])
    
    return output_path
