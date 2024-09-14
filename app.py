from flask import Flask, jsonify
import threading
import joycon_module  # 修正したファイル名に合わせてインポート

app = Flask(__name__)

# Joy-Conのデータを保持する変数
joycon_data = {"accel": {}, "score": 0}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/joycon')
def get_joycon_data():
    global joycon_data  # グローバル変数を参照
    print("Joy-Con data request received")
    # 現在のJoy-Conデータを返す
    return jsonify(joycon_data)

def start_joycon_data_acquisition():
    global joycon_data
    joycon_module.start_joycon_data_acquisition(joycon_data)

if __name__ == '__main__':
    # Joy-Conのデータ取得を別スレッドで開始
    joycon_thread = threading.Thread(target=start_joycon_data_acquisition)
    joycon_thread.daemon = True
    joycon_thread.start()

    # Flaskサーバーをポート5001で実行
    app.run(port=5001)
