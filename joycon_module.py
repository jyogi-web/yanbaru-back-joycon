from pyjoycon import JoyCon, get_R_id
import time
from datetime import datetime

# 得点を初期化
score = 0

def start_joycon_data_acquisition():
    try:
        joycon_id = get_R_id()
        joycon = JoyCon(*joycon_id)

        prev_accel = {'x': 0, 'y': 0, 'z': 0}

        start_time = datetime.now()

        while True:
            status = joycon.get_status()
            accel = status['accel']

            accel_change = abs(accel['x'] - prev_accel['x'])

            if accel_change > 3000:
                score += 10  
                print(f"Joy-Conを振りました！得点: {score}")

            prev_accel = accel

            print("加速度:", accel)
            time.sleep(0.1)
            endtime = datetime.now()
            dlapsedtime = endtime - start_time 
            print("経過時間：", dlapsedtime)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
