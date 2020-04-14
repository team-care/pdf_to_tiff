import uvicorn
from fastapi import FastAPI, File, UploadFile
from pdf2image import convert_from_bytes
from base64 import b64encode
import os

api = FastAPI()


@api.post("/")
async def post(file: UploadFile = File(...)):
    buffer = await file.read()
    test = convert(file.filename, buffer)
    return {"file": test}


def convert(filename, file):
    output_path = f"./data/{filename}.tif"
    images = convert_from_bytes(file)
    images = [i.convert("1") for i in images]
    images[0].save(
        output_path,
        format='TIFF',
        dpi=(400, 400),
        compression="group4",
        save_all=True,
        append_images=images[1:])
    with open(output_path, "rb") as f:
        tiff_data = b64encode(f.read())
    os.remove(output_path)
    return tiff_data


if __name__ == "__main__":
    uvicorn.run(api)
