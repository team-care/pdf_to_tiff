import base64
import json
import os
import shutil
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)


class Utils:
    def __init__(self):
        self._temp_dir = "/tmp/data/"
        self._required_required_content_type = "application/pdf"
        self._required_input_extention = "pdf"
        self._required_output_extention = "tif"

    def json_parse(self, json_string):
        if isinstance(json_string, str):
            return json.loads(json_string)
        return json_string

    def get_content_type_from_header(self, headers):
        if headers.get("Content-Type"):
            return headers.get("Content-Type")
        elif headers.get("content-type"):
            return headers.get("content-type")

    def get_input_filename_from_header(self, headers):
        if headers.get("InputFileName"):
            return headers.get("InputFileName")
        elif headers.get("inputfilename"):
            return headers.get("inputfilename")

    def get_output_file_extention_from_header(self, headers):
        if headers.get("OutputFileExtention"):
            return headers.get("OutputFileExtention")
        elif headers.get("outputfileextention"):
            return headers.get("outputfileextention")

    def validate_content_type(self, content_type):
        if content_type != self._required_required_content_type:
            message = f"Content-Type is not {self._required_required_content_type}"
            logger.warning(message)
            raise LambdaRuntimeException(400, message)
        logger.info(f"Content-Type is {content_type}")

    def validate_input_filename(self, input_filename):
        if "\\" in input_filename or "/" in input_filename:
            message = "Invalid request parameter"
            logger.warning(message)
            raise LambdaRuntimeException(400, message)
        logger.info(f"Input filename is {input_filename}")

    def validate_input_file_extention(self, input_filename):
        extention = Path(input_filename).suffix
        if extention != f".{self._required_input_extention}":
            message = f"Input file extention is not {self._required_input_extention}"
            logger.warning(message)
            raise LambdaRuntimeException(400, message)
        logger.info(f"Input file extention is {extention}")

    def validate_output_file_extention(self, output_extention):
        if output_extention != self._required_output_extention:
            message = f"Output file extention is not {self._required_output_extention}"
            logger.warning(message)
            raise LambdaRuntimeException(400, message)
        logger.info(f"Output file extention is {output_extention}")

    def make_temp_dir(self):
        if os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)
        os.makedirs(self._temp_dir)
        logger.info(f"Make directory {self._temp_dir}")

    def save_input_file(self, input_filename, input_file):
        save_file_path = f"{self._temp_dir}{input_filename}"
        with open(save_file_path, "wb") as f:
            f.write(base64.b64decode(input_file.encode("utf8")))
        logger.info(f"Save input file {save_file_path}")
        return save_file_path

    def change_extention(self, input_file_path, extention="tif"):
        output_file_path = Path(input_file_path).with_suffix(f".{extention}")
        logger.info(f"Output file path is {output_file_path}")
        return str(output_file_path)

    def success_response(self, output_file, code=200, content_type="application/pdf", encode=True):
        response = {
            "statusCode": code,
            "headers": {
                "content-type": content_type
            },
            "isBase64Encoded": encode,
            "body": base64.b64encode(output_file)
        }
        return response


class LambdaRuntimeException(Exception):
    def __init__(self, code, messages, content_type="application/json"):
        self._code = code
        self._messages = messages
        self._content_type = content_type

    def __str__(self):
        response = {
            "statusCode": self._code,
            "headers": {
                "Content-Type": self._content_type
            },
            "body": {
                "message": self._messages
            }
        }
        return json.dumps(response)
