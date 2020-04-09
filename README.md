# PDF to TIFF

PDF画像を(白黒=grayscaleの)TIFFへ変換するサンプルです。

Dependency

* [pdf2image](https://github.com/Belval/pdf2image)

## How to run

変換後の形式は以下になります。
- 解像度：400 dpi
- ファイル形式：マルチTIF
- カラー：グレースケール
- 圧縮形式：deflate

※圧縮形式はG4にしたい

### Lambda Style

![lambda_style.PNG](./docs/lambda_style.PNG)
※現在は上記の仕様を満たしていません。

1. Dockerを利用できる環境を用意する。

2. 以下のコマンドを順番に実行してAWS Lambdaにデプロイするパッケージを作成する。
    ```
    docker build -t pdf-to-tiff-for-lambda -f Dockerfile.lambda .
    docker run -d --name package-build pdf-to-tiff-for-lambda
    docker cp package-build:deploy.zip .
    docker rm package-build
    ```

3. AWS Lambdaに作成した`deploy.zip`をアップロードする。

    ランタイム：Python3.8  
    ハンドラ：main.handler

4. 以下のコマンドで動作確認が可能
    ```
    aws lambda invoke --function-name Lambda関数名 test.tif
    ```
    ※Lambda関数内のpdfがtiffに変換されて`test.tif`として返却される。

### Fargate Style

![fargate_style.PNG](./docs/fargate_style.PNG)
※現在は上記の仕様を満たしていません。

1. Dockerを利用できる環境を用意する。

2. 以下のコマンドを実行してAWS Lambdaにデプロイするパッケージを作成する。
    ```
    docker build -t pdf-to-tiff-for-fargate -f Dockerfile.fargate .
    ```

3. 以下のコマンドを順番に実行してローカルで動作確認を行う
    1. dockerコンテナを起動
        ```
        docker run --rm -it -p 8000:80 pdf-to-tiff-for-fargate
        ```

    2. dockerコンテナのAPIサーバーにリクエスト
        ```
        curl -X POST --noproxy localhost -F 'Filename=./data/tis_200206.pdf' -F 'file=@./data/tis_200206.pdf' http://localhost:8000 | jq -r '.file' | base64 -di > ./test.tif
        ```
        ※jqコマンドを使用できるようにしておく必要がある。
        <details><summary>python requests</summary><div>

        ```python:python requests
        import os
        import requests
        import base64

        os.environ['NO_PROXY'] = 'localhost'
        filename = "tis_200206"

        with open(f"./data/{filename}.pdf", "rb") as f:
            pdf = f.read()
        files = {'file': (filename, pdf)}
        r = requests.post("http://localhost:8000", files=files)
        data = base64.b64decode(r.json()["file"])

        with open(f"./test.tif", "wb") as f:
            f.write(data)

        ```
        </div></details>
        ※pdfがtiffに変換されて`test.tif`として返却される。

    3. dockerイメージをECRにpushする...
        以降は未検証

#### Development

VSCodeの[Remote Containers](https://code.visualstudio.com/docs/remote/containers)機能を使用しています。

* [Getting started](https://code.visualstudio.com/docs/remote/containers#_getting-started)の通りにセットアップ
* F1ボタンを押して[Remote-Containers: Add Development Container Configuration~](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container)を選択。`Dockerfile.dev`を選択してconfigurationを作成。
  * 初回はコンテナの作成に時間がかかる
* Terminalを開くと、コンテナ内で開ける。

以下のコマンドで変換結果を確認可能。

```
python convert.py data/tis_200206.pdf
```
