FROM python:2.7.13-alpine
MAINTAINER idiamond@ucsd.edu

COPY . /data/src

WORKDIR /data/src

RUN pip install Flask && pip install textblob

ENV FLASK_APP analysis.py

RUN mkdir -p /data/_cache && echo "{}" > /data/_cache/cache
ENV CACHE_LOCATION /data/_cache/cache

CMD ["flask", "run", "--host=0.0.0.0"]

