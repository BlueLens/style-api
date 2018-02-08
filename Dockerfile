#FROM bluelens/tensorflow:1.3.0-py3
FROM bluelens/ubuntu-16.04:py3

RUN mkdir -p /opt/app/model
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

ENV LANG en_US.UTF-8

EXPOSE 8080
ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
#CMD ["dummy.py"]
