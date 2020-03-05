FROM python:3.7.6-slim

WORKDIR /work

# ライブラリインストール
COPY Pipfile Pipfile.lock ./

RUN apt-get update && apt-get -y install build-essential && \
    pip install --no-cache-dir --upgrade pip pipenv && \
    pipenv install --system && \
    rm -f Pipfile Pipfile.lock

# アプリケーションビルド
COPY manage.py entrypoint.sh .env ./
COPY babinizer/ babinizer/
COPY app/ app/

ENTRYPOINT ["sh", "entrypoint.sh"]
