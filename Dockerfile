FROM lambci/lambda:build-python3.8

# 必要なライブラリインストール
RUN yum update -y && \
    yum install -y \
    poppler-utils

COPY src/main /package
COPY requirements.txt /work/requirements.txt
COPY config/logging.conf /work/config/logging.conf
COPY entrypoint.sh /work/entrypoint.sh

WORKDIR /work
ENTRYPOINT [ "bash", "entrypoint.sh" ]