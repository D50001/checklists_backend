FROM python:3.11-slim

RUN apt update && apt upgrade -y

ARG UID=1000
ARG GID=1000

#RUN groupadd -g ${GID} prod && useradd -rms /bin/bash -u ${UID} -g ${UID} prod && chmod 777 /opt /run
RUN addgroup -g ${GID} prod && adduser -u ${UID} -G prod -s /bin/sh -D prod

WORKDIR /app

RUN chown -R ${GID}:${UID} /app && chmod 755 /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=${GID}:${UID} auto_checklist/ .