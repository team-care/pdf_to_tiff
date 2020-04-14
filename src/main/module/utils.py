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

    def json_parse(self, json_string):
        if isinstance(json_string, str):
            return json.loads(json_string)
        return json_string

    def validate_input_key_extention(self, input_key):
        extention = Path(input_key).suffix
        if extention != f".{self._required_input_extention}":
            message = f"Input key extention is not {self._required_input_extention}"
            logger.warning(message)
            raise LambdaRuntimeException(400, message)
        logger.info(f"Input key extention is {extention}")

    def make_temp_dir(self):
        if os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)
        os.makedirs(self._temp_dir)
        logger.info(f"Make directory {self._temp_dir}")
        return self._temp_dir

    def change_extention(self, input_key, extention="tif"):
        output_filename = Path(input_key).with_suffix(f'.{extention}').name
        logger.info(f"Output filename is {output_filename}")
        return output_filename

    def success_response(self, message, code=200, content_type='application/pdf'):
        response = {
            'statusCode': code,
            'headers': {
                'content-type': content_type
            },
            'body': {
                "message": message
            }
        }
        return response

class LambdaRuntimeException(Exception):
    def __init__(self, code, messages, content_type='application/json'):
        self._code = code
        self._messages = messages
        self._content_type = content_type

    def __str__(self):
        response = {
            'statusCode': self._code,
            'headers': {
                'Content-Type': self._content_type
            },
            'body': {
                'message': self._messages
           }
        }
        return json.dumps(response)
