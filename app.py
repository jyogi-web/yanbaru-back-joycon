# app.py
from flask import Flask
import threading
import joycon_module  # 修正したファイル名に合わせてインポート

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/joycon')
def get():
    print("joycon")
    # Joy-Conデータ取得を開始する関数を呼び出す
    return "Joy-Con data acquisition started."

def start_joycon_data_acquisition():
    joycon_module.start_joycon_data_acquisition()

if __name__ == '__main__':
    # Joy-Conのデータ取得を別スレッドで開始
    joycon_thread = threading.Thread(target=start_joycon_data_acquisition)
    joycon_thread.daemon = True
    joycon_thread.start()

    # Flaskサーバーをポート5001で実行
    app.run(port=5001)
