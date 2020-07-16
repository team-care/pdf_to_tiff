import os
from logging.config import fileConfig
from logging import getLogger
from module import PDFtoTIFFConverter, S3Controller, Utils


def handler(event, context):
    # logger設定
    fileConfig(
        f"{os.path.dirname(os.path.abspath(__file__))}/config/logging.conf",
        disable_existing_loggers=False)
    logger = getLogger(__name__)

    # popplerのバイナリとライブラリにpathを通す
    os.environ["PATH"] += \
        f":{os.path.dirname(os.path.abspath(__file__))}/bin/"
    os.environ["LD_LIBRARY_PATH"] += \
        f":{os.path.dirname(os.path.abspath(__file__))}/lib/"

    # 使用するS3バケット名を環境変数から読み込む
    s3_bucket_name = os.environ.get("S3_BUCKET_NAME")

    # クラスインスタンス生成
    utils = Utils()
    s3_controller = S3Controller()
    converter = PDFtoTIFFConverter()

    # 入力情報取得
    input_event = utils.json_parse(
        json_string=event)
    request_body = utils.json_parse(
        json_string=input_event["body"])
    key = request_body["key"]

    # 一時ディレクトリ作成
    pdf_dir = utils.make_temp_dir(
        dir_name="pdf")
    tif_dir = utils.make_temp_dir(
        dir_name="tif")

    # S3からPDFを取得
    pdf_path = s3_controller.download(
        bucket_name=s3_bucket_name,
        key=key,
        save_dir=pdf_dir)

    # TIFF変換
    tif_path = converter.convert(
        pdf_path=pdf_path,
        output_dir=tif_dir,
        filename=key)

    # S3に同名ファイルが存在する場合はエラー
    s3_controller.error_if_object_exists(
        bucket_name=s3_bucket_name,
        file_dir="tif",
        filename=f"{key}.tif")

    # S3にアップロード
    s3_controller.upload(
        filepath=tif_path,
        bucket_name=s3_bucket_name,
        upload_dir="tif",
        filename=f"{key}.tif",
        content_type='image/tiff')

    # 念のためにローカルのファイルを削除
    os.remove(pdf_path)
    os.remove(tif_path)
    logger.info("success")
    return utils.success_response("success")
