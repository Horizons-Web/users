FROM python:3.11-alpine

WORKDIR /users-ms

COPY requirements.txt .

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* \
    && rm -rf requirements.txt

COPY . .

