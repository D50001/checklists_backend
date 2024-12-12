FROM python:3.11-slim

RUN apt update && apt upgrade -y

RUN groupadd -g 1000 prod && useradd -rms /bin/bash -u 1000 -g 1000 prod && chmod 777 /opt /run

WORKDIR /app

RUN chown -R prod:prod /app && chmod 755 /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=prod:prod auto_checklist/ .