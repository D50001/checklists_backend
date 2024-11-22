FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG USER
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER ${USER}

COPY auto_checklist/ .