FROM python:3.7

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

COPY .env /app/.env
COPY ./misc /app/misc

RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /app/misc/loop_installation.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

COPY ./src/generator/requirements.txt /app/src/generator/requirements.txt
COPY ./src/misc/requirements.txt /app/src/misc/requirements.txt


RUN cd /app && bash /app/misc/loop_installation.sh

COPY ./src/generator /app/src/generator
COPY ./src/misc /app/src/misc
COPY ./src/__init__.py /app/src/__init__.py

WORKDIR /app

ENTRYPOINT ["python"]