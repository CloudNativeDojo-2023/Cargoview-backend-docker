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

# 公開鍵認証のためのディレクトリを作成
RUN mkdir -p /home/test/.ssh

# 公開鍵をコピー
COPY ./key/id_rsa.pub /home/test/.ssh/authorized_keys

# テスト用アカウントtestのホームディレクトリの所有者をtestに変更
RUN chown -R test:test /home/test

# テスト用アカウントtestのホームディレクトリのパーミッションを変更
RUN chmod 700 /home/test/.ssh && chmod 600 /home/test/.ssh/authorized_keys

# SSHサーバーの設定ファイルをコピー
COPY ./cfg/sshd_config /etc/ssh/sshd_config

# sshdサービス起動用のスクリプトをコピー
COPY ./cfg/init.sh /init.sh
RUN chmod +x /init.sh
