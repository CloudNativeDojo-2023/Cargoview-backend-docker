# ベースイメージを指定
FROM python:3.10-slim

# 基本的なパッケージのインストールとアップグレード
RUN apt update && apt upgrade -y

# pipのインストール
RUN python3 -m pip install -U pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY modules/* ./modules
CMD ["python3", "main.py"]
