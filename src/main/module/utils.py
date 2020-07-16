import json
import os
import shutil
from logging import getLogger

logger = getLogger(__name__)


class Utils:
    def __init__(self):
        self._temp_dir = "/tmp"

    def json_parse(self, json_string):
        if isinstance(json_string, str):
            return json.loads(json_string)
        return json_string

    def make_temp_dir(self, dir_name):
        dir_name = f"{self._temp_dir}/{dir_name}"
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)
        logger.info(f"Make directory {dir_name}")
        return dir_name

    def success_response(self, message, code=200,
                         content_type='application/pdf'):
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
