from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import joycon_module

app = Flask(__name__)
socketio = SocketIO(app)

# Joy-Conのデータを保持するグローバル変数
joycon_data = {"accel": {}, "score": 0}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/joycon')
def get_joycon_data():
    global joycon_data
    return jsonify(joycon_data)

def start_joycon_data_acquisition():
    global joycon_data
    joycon_module.start_joycon_data_acquisition(joycon_data)

def joycon_data_update_thread():
    while True:
        socketio.emit('joycon_update', joycon_data)
        socketio.sleep(0.5)

if __name__ == '__main__':
    # Joy-Conのデータ取得を別スレッドで開始
    joycon_thread = threading.Thread(target=start_joycon_data_acquisition)
    joycon_thread.daemon = True
    joycon_thread.start()

    # WebSocketのデータ送信スレッドを開始
    socketio.start_background_task(target=joycon_data_update_thread)

    socketio.run(app, port=5001)
