from pdf2image import convert_from_bytes
from logging import getLogger
from .utils import Utils, LambdaRuntimeException
from .s3_controller import S3Controller

logger = getLogger(__name__)


class PDFtoTIFFConverter:
    def __init__(self):
        self._utils = Utils()
        self._s3_controller = S3Controller()

    def execution(self, event, context):
        try:
            # 入力情報取得
            input_data = self._utils.json_parse(event)
            body = self._utils.json_parse(input_data["body"])
            input_key = body["input_key"]

            # 入力キー確認
            self._utils.validate_input_key_extention(input_key)

            # S3からPDF取得
            pdf_data = self._s3_controller.get_s3_object(input_key)

            # 一時フォルダ作成
            temp_dir = self._utils.make_temp_dir()

            # 出力ファイル名作成
            output_filename = self._utils.change_extention(input_key)

            # tifに変換
            output_path = f"{temp_dir}{output_filename}"
            tif_data = self._convert(pdf_data, output_path)

            # s3に保存
            output_key = self._s3_controller.put_s3_object(
                tif_data, output_filename)

            # 成功応答
            return self._utils.success_response(f"Save tif data {output_key}")
        except LambdaRuntimeException as e:
            # 想定内エラーをraise
            raise e
        except Exception:
            # 予期しないエラーをraise
            message = "Unexpected Error"
            logger.exception(message)
            raise LambdaRuntimeException(503, message)

    def _convert(self, pdf_data, output_path, output_format="TIFF", dpi=400, compression="group4"):
        try:
            # PDFからtifに変換
            images = convert_from_bytes(pdf_data)
            # 白黒に変換
            images = [i.convert("1") for i in images]
            # マルチページTIFFに変換して保存
            images[0].save(
                output_path,
                format=output_format,
                dpi=(dpi, dpi),
                compression=compression,
                save_all=True,
                append_images=images[1:])
            # 変換したファイルを読み込み
            with open(output_path, "rb") as f:
                output_file = f.read()
            logger.info(f"Convert Success. Save {output_path}")
            return output_file
        except Exception:
            message = "Failed convert pdf to tiff"
            logger.exception(message)
            raise LambdaRuntimeException(503, message)
