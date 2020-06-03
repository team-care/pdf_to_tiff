FROM amazonlinux:2

# 必要なライブラリインストール
RUN yum update -y && \
    yum install -y \
    bzip2-devel \
    gcc \
    libopenjp2-7 \
    libffi-devel \
    make \
    mlocate \
    openssl-devel \
    poppler-utils \
    tar \
    wget \
    which \
    zip
RUN updatedb

# python3.8 インストール
RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz && \
    tar xvf Python-3.8.2.tgz && \
    cd Python-3.8*/ && \
    ./configure --enable-optimizations && \
    make altinstall

# Pythonのシンボリックリンクを編集
RUN ln -nfs /usr/local/bin/pip3.8 /usr/local/bin/pip && \
    ln -nfs /usr/local/bin/python3.8 /usr/local/bin/python

# 作業ディレクトリ作成
RUN rm -rf /package && \
    mkdir -p /package/poppler/ && \
    mkdir -p /package/config/

# Lambda function用のzip作成
RUN cp -Rf $(which pdfdetach) /package/poppler/ && \
    cp -Rf $(which pdffonts) /package/poppler/ && \
    cp -Rf $(which pdfimages) /package/poppler/ && \
    cp -Rf $(which pdfinfo) /package/poppler/ && \
    cp -Rf $(which pdfseparate) /package/poppler/ && \
    cp -Rf $(which pdftocairo) /package/poppler/ && \
    cp -Rf $(which pdftohtml) /package/poppler/ && \
    cp -Rf $(which pdftoppm) /package/poppler/ && \
    cp -Rf $(which pdftops) /package/poppler/ && \
    cp -Rf $(which pdftotext) /package/poppler/ && \
    cp -Rf $(which pdfunite) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libpoppler) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libjpeg) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libtiff) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libpng15) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libopenjpeg) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/liblcms) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libfontconfig) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libfreetype) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libjbig) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libexpat) /package/poppler/ && \
    cp -Rf $(locate /usr/lib64/libz) /package/poppler/
COPY src/binary_type /package
COPY config/logging.conf /package/config
COPY config/requirements.txt .
RUN pip install -r requirements.txt -t /package/
RUN cd /package && \
    zip -r9 /deploy.zip .
