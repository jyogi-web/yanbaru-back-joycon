from pyjoycon import JoyCon, get_R_id
import time

# 左Joy-Conの取得
joycon_id = get_R_id()
joycon = JoyCon(*joycon_id)

while True:
    # ジャイロデータを取得
    gyro = joycon.get_status()['gyro']
    accel = joycon.get_status()['accel']

    # 加速度データ
    accel_x = accel['x']
    accel_y = accel['y']
    accel_z = accel['z']

    # データ表示
    print(f"加速度: X: {accel_x}, Y: {accel_y}, Z: {accel_z}")
    print(f"ジャイロ: X: {gyro['x']}, Y: {gyro['y']}, Z: {gyro['z']}")

    time.sleep(0.1)
