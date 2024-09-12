from flask import Flask, jsonify
from pyjoycon import JoyCon, get_L_id  
import threading
import time

app = Flask(__name__)

# Joy-Conのデータを格納するための辞書
joycon_data = {
    "accel_x": 0,
    "accel_y": 0,
    "accel_z": 0,
    "gyro_x": 0,
    "gyro_y": 0,
    "gyro_z": 0
}

# Joy-Conデータ取得用のスレッドを定義
def joycon_thread():
    try:
        joycon_id = get_L_id()  # 左Joy-ConのIDを取得
        joycon = JoyCon(*joycon_id)

        while True:
            status = joycon.get_status()
            accel = status['accel']
            gyro = status['gyro']

            # 取得したデータを辞書に格納
            joycon_data['accel_x'] = accel['x']
            joycon_data['accel_y'] = accel['y']
            joycon_data['accel_z'] = accel['z']
            joycon_data['gyro_x'] = gyro['x']
            joycon_data['gyro_y'] = gyro['y']
            joycon_data['gyro_z'] = gyro['z']

            time.sleep(0.1)
    except Exception as e:
        print("Error connecting to Joy-Con:", e)

# Joy-Conのデータ取得スレッドを開始
threading.Thread(target=joycon_thread, daemon=True).start()

@app.route('/')
def index():
    return jsonify(joycon_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
