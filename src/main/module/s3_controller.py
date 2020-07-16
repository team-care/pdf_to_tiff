import boto3
from logging import getLogger
from .utils import LambdaRuntimeException


class S3Controller:
    def __init__(self):
        self._logger = getLogger(__name__)
        self._s3_resource = boto3.resource('s3')

    def download(self, bucket_name, key, save_dir):
        filepath = f"{save_dir}/{key}"
        try:
            self._s3_resource.Object(bucket_name, key).download_file(filepath)
            self._logger.info(
                f"Download from S3://{bucket_name}/{key} to {filepath}")
            return filepath
        except Exception:
            message = f"Failed to download S3://{bucket_name}/{key}."
            self._logger.error(message)
            raise LambdaRuntimeException(503, message)

    def upload(self, filepath, bucket_name,
               upload_dir, filename, content_type):
        key = f"{upload_dir}/{filename}"
        try:
            self._s3_resource.Object(bucket_name, key).upload_file(filepath)
            self._logger.info(
                f"Upload from {filepath} to S3://{bucket_name}/{key}")
        except Exception:
            message = f"Failed to upload S3://{bucket_name}/{key}."
            self._logger.error(message)
            raise LambdaRuntimeException(503, message)

    def error_if_object_exists(self, bucket_name, file_dir, filename):
        key = f"{file_dir}/{filename}"
        try:
            self._s3_resource.Object(bucket_name, key).load()
            message = f"Object already exists S3://{bucket_name}/{key}."
            self._logger.error(message)
            raise LambdaRuntimeException(503, message)
        except LambdaRuntimeException as e:
            raise e
        except Exception:
            self._logger.info(
                f"Object does not exist S3://{bucket_name}/{key}.")
