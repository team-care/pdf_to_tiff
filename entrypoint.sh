#!bin/bash
# パス定義
BIN_PATH=/package/bin
LIB_PATH=/package/lib
CONF_PATH=/package/config

# フォルダとファイルの整理
rm -rf *.zip
mkdir -p $BIN_PATH
mkdir -p $LIB_PATH
mkdir -p $CONF_PATH

# binとlibの収集
bin_array=(`find /usr/bin/ -name pdf*`)
for i in ${bin_array[@]}; do
    cp $i $BIN_PATH
    lib_array=(`ldd $i | grep "=>" | awk '{print $1}'`)
    for j in ${lib_array[@]}; do
        cp /usr/lib64/$j $LIB_PATH
    done
done

# 設定ファイルの配置
cp ./requirements.txt /package/
cp ./config/logging.conf /package/config/

# ソースコードの配置
cp -rf ./src/main/* /package/

# バイナリを直接変換する場合はこちらをコメント解除
# cp -rf ./src/binary_type/* /package/

# デプロイパッケージの作成
cd /package/
pip install -r requirements.txt -t .
rm -rf `find ./ -name "*__pycache__*"` \
        `find ./ -name "*dist-info*"` \
        `find ./ -name "test"` \
        `find ./ -name "tests"`
zip -r9 /work/deploy.zip .
