
FROM python:3.8.5

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python -m nltk.downloader all

COPY . /app

EXPOSE 8000
EXPOSE 80
