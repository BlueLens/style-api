FROM bluelens/tensorflow:1.3.0-py3

RUN mkdir -p /opt/app/model
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN curl https://s3.ap-northeast-2.amazonaws.com/bluelens-style-model/classification/inception_v3/classify_image_graph_def.pb -o /opt/app/model/classify_image_graph_def.pb
ENV CLASSIFY_GRAPH=/opt/app/model/classify_image_graph_def.pb

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

ENV LANG en_US.UTF-8

EXPOSE 8080
ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]