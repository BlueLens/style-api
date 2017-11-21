FROM python:3-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

#COPY . /usr/src/app

#RUN apt-get install ca-certificates libffi6 libstdc++ && \
#    apt-get install --virtual build-deps build-base libffi-dev && \
#RUN pip install --no-cache-dir gunicorn /usr/src/app

#EXPOSE 8080
#
#CMD ["gunicorn", "-k", "gevent", "--timeout", "200", "-b", "0.0.0.0:8080", "bl_db_product:app"]

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]