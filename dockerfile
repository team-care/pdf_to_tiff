FROM amazonlinux:2
RUN yum update -y && \
    yum install -y \
    libopenjp2-7 \
    mlocate \
    poppler-utils \
    python3 \
    which \
    zip
RUN rm -rf /package && \
    mkdir -p /package/poppler/
RUN updatedb
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
    cp -Rf $(locate libpoppler.so) /package/poppler/ && \
    cp -Rf $(locate libjpeg.so) /package/poppler/ && \
    cp -Rf $(locate libtiff.so) /package/poppler/ && \
    cp -Rf $(locate libpng15.so) /package/poppler/ && \
    cp -Rf $(locate libopenjpeg.so) /package/poppler/ && \
    cp -Rf $(locate libz.so) /package/poppler/
ADD requirements.txt .
RUN pip3 install -r requirements.txt -t /package/
ADD lambda_function /package
RUN cd /package && \
    zip -r9 /deploy.zip .
