FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/app

# Install dependencies
RUN apt-get update -yy \
    && apt-get upgrade -yy \
    && apt-get install -yy libpq-dev \
    && pip install --no-cache-dir --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]