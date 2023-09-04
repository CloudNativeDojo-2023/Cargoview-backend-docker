# ベースイメージを指定
FROM python:3.10-slim

# 基本的なパッケージのインストールとアップグレード
RUN apt update && apt upgrade -y

# pipのインストール
RUN python3 -m pip install -U pip

# テスト用アカウントtestを作成
RUN adduser --disabled-password --gecos "" test

# テスト用アカウントtestのパスワードを設定
RUN echo "test:test" | chpasswd

# テスト用アカウントtestをsudoグループに追加
RUN usermod -aG sudo test

WORKDIR /app

#COPY requirements.txt
COPY ./backend/requirements.txt /app/
RUN pip install -r /app/requirements.txt

RUN mkdir -p /upload

RUN chown -R test:test /upload && chmod 777 /upload

COPY ./backend/main.py /app/

COPY ./backend/modules /app/modules
