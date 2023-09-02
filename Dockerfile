# ベースイメージを指定
FROM python:3.10-slim

# 基本的なパッケージのインストールとアップグレード
RUN apt update && apt upgrade -y

# pipのインストール
RUN python3 -m pip install -U pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
#監視対象ディレクトリの作成
RUN mkdir test
#テスト用に権限関係の問題を無視するための措置
RUN chmod 777 /app /app/test
COPY main.py .
COPY modules/* ./modules
CMD ["python3", "main.py"]
