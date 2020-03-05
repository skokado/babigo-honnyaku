FROM python:3.7.6-slim

# ホスト環境変数のマッピング
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

WORKDIR /work

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
