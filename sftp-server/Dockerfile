# ベースイメージを指定
FROM ubuntu:22.04

# 基本的なパッケージのインストールとアップグレード
RUN apt update && apt upgrade -y

# openssh-serverをインストール
RUN apt install openssh-server -y

# テスト用アカウントtestを作成
RUN adduser --disabled-password --gecos "" test

# テスト用アカウントtestのパスワードを設定
RUN echo "test:test" | chpasswd

# テスト用アカウントtestをsudoグループに追加
RUN usermod -aG sudo test

# テスト用アカウントtestのホームディレクトリの所有者をtestに変更
RUN chown -R test:test /home/test

# SSHサーバーの設定ファイルをコピー
COPY ./sftp-server/cfg/sshd_config /etc/ssh/sshd_config

# sshdサービス起動用のスクリプトをコピー
COPY ./sftp-server/cfg/init.sh /init.sh
RUN chmod +x /init.sh

RUN mkdir -p /upload

RUN chown -R test:test /upload && chmod 777 /upload
