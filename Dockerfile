# Python 3.8のベースイメージを使用
FROM python:3.8-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    libhidapi-hidraw0 libhidapi-libusb0 libusb-1.0-0-dev \
    bluetooth libbluetooth-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python用のhidapiライブラリのインストール
RUN pip install hidapi

# 作業ディレクトリを作成
WORKDIR /app

# アプリケーションファイルをコピー
COPY app /app

# 依存関係をインストール
RUN pip install --no-cache-dir -r /app/requirements.txt

# コンテナ起動時の実行コマンド
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001", "--reload"]
