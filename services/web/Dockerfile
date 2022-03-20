FROM python:3.9-slim-buster

WORKDIR src/web_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /src/web_app/

ENTRYPOINT ["/src/web_app/entrypoint.sh"]
