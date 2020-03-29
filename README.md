# PDF to TIFF

PDF画像を(白黒=grayscaleの)TIFFへ変換するサンプルです。

## How to run

### Development

VSCodeの[Remote Containers](https://code.visualstudio.com/docs/remote/containers)機能を使用しています。

* [Getting started](https://code.visualstudio.com/docs/remote/containers#_getting-started)の通りにセットアップ
* F1ボタンを押して[Remote-Containers: Add Development Container Configuration~](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container)を選択。`Dockerfile.dev`を選択してconfigurationを作成。
  * 初回はコンテナの作成に時間がかかる
* Terminalを開くと、コンテナ内で開ける。

以下のコマンドで変換結果を確認可能。

```
python convert.py data/tis_200206.pdf
```


### Production


## Dependency

* [pdf2image](https://github.com/Belval/pdf2image)

