# PDF to TIFF

PDF画像を(白黒=grayscaleの)TIFFへ変換するサンプルです。

Dependency

* [pdf2image](https://github.com/Belval/pdf2image)

## How to run

### Lambda Style

![lambda_style.PNG](./docs/lambda_style.PNG)

1. Dockerを利用できる環境を用意する。

2. 以下のコマンドを順番に実行してAWS Lambdaにデプロイするパッケージを作成する。
    ```
    docker build -t pdf-to-tiff -f Dockerfile.lambda .
    docker run -d --name package-build pdf-to-tiff
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
