FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/app

# Install dependencies
RUN apt-get update -yy \
    && apt-get upgrade -yy \
    && apt-get install -yy libpq-dev gcc g++ make

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .