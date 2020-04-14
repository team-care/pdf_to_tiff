from pdf2image import convert_from_path
from logging import getLogger
from .utils import Utils, LambdaRuntimeException

logger = getLogger(__name__)


class PDFtoTIFFConverter:
    def __init__(self):
        self._utils = Utils()

    def execution(self, event, context):
        try:
            # 入力情報取得
            input_data = self._utils.json_parse(event)
            content_type = self._utils.get_content_type_from_header(
                input_data["headers"])
            input_filename = self._utils.get_input_filename_from_header(
                input_data["headers"])
            output_file_extention = self._utils.get_output_file_extention_from_header(
                input_data["headers"])
            input_file = input_data["body"]

            # content-type確認
            self._utils.validate_content_type(content_type)

            # 入力ファイル名確認
            self._utils.validate_input_filename(input_filename)

            # 入力ファイル拡張子確認
            self._utils.validate_input_file_extention(input_filename)

            # 出力ファイル拡張子確認
            self._utils.validate_output_file_extention(output_file_extention)

            # 一時ファイル作成
            self._utils.make_temp_dir()

            # 一時ファイルにPDFを保存
            input_file_path = self._utils.save_input_file(
                input_filename, input_file)

            # tifに変換
            tif_data = self._convert(input_file_path)

            # 成功応答
            return self._utils.success_response(tif_data)
        except LambdaRuntimeException as e:
            # 想定内エラーをraise
            raise e
        except Exception:
            # 予期しないエラーをraise
            message = "Unexpected Error"
            logger.exception(message)
            raise LambdaRuntimeException(503, message)

    def _convert(self, input_file_path, output_format="TIFF", dpi=400, compression="group4"):
        try:
            # PDFからtifに変換
            images = convert_from_path(input_file_path)
            # 白黒に変換
            images = [i.convert("1") for i in images]
            # マルチページTIFFに変換して保存
            output_file_path = self._utils.change_extention(input_file_path)
            images[0].save(
                output_file_path,
                format=output_format,
                dpi=(dpi, dpi),
                compression=compression,
                save_all=True,
                append_images=images[1:])
            # 変換したファイルを読み込み
            with open(output_file_path, "rb") as f:
                output_file = f.read()
            logger.info(f"Convert Success. Save {output_file_path}")
            return output_file
        except Exception:
            message = "Failed convert pdf to tiff"
            logger.exception(message)
            raise LambdaRuntimeException(503, message)
