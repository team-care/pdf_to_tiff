import boto3
import os
from logging import getLogger
from .utils import LambdaRuntimeException

logger = getLogger(__name__)


class S3Controller:
    def __init__(self):
        self._s3_resource = boto3.resource('s3')
        self._s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
        self._s3_output_prefix = "tif/"

    def put_s3_object(self, data, output_filename, content_type='image/tiff'):
        try:
            output_key = f"{self._s3_output_prefix}{output_filename}"
            obj = self._s3_resource.Object(self._s3_bucket_name, output_key)
            obj.put(
                Body=data,
                ContentType=content_type
            )
            logger.info(f"Put object {output_key}")
            return output_key
        except Exception:
            message = "Failed put s3 object"
            logger.error(message)
            raise LambdaRuntimeException(503, message)
