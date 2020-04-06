# PDF to TIFF

PDF画像を(白黒=grayscaleの)TIFFへ変換するサンプルです。

## How to run

### Development

1. Dockerを利用できる環境を用意する。

2. 以下のコマンドを順番に実行してAWS Lambdaにデプロイするパッケージを作成する。
    ```
    docker build -t pdf-to-itff .
    docker run -d --name package-build pdf-to-itff
    docker cp package-build:deploy.zip .
    docker rm package-build
    ```

3. AWS Lambdaに作成した`deploy.zip`をアップロードする。

    ランタイム：Python3.7

    ハンドラ：main.handler

4. 以下のコマンドで動作確認が可能
    ```
    aws lambda invoke --function-name Lambda関数名 test.tif
    ```
    ※Lambda関数内のpdfがtiffに変換されて`test.tif`として返却される。

### Production


## Dependency

* [pdf2image](https://github.com/Belval/pdf2image)

