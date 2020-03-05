FROM python:3.7.6-slim

WORKDIR /work
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

# ライブラリインストール
COPY Pipfile Pipfile.lock ./

RUN apt-get update && apt-get -y install build-essential && \
    pip install --no-cache-dir --upgrade pip pipenv && \
    pipenv install --system && \
    rm -f Pipfile Pipfile.lock

# アプリケーションビルド
COPY manage.py entrypoint.sh ./
COPY babinizer/ babinizer/
COPY app/ app/

EXPOSE 8001
ENTRYPOINT ["sh", "entrypoint.sh"]
