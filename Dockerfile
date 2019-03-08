FROM python:alpine
WORKDIR /usr/src/spider
RUN apk add --no-cache build-base libxml2-dev libxslt-dev openssl-dev libffi-dev curl && \
    pip install scrapy
