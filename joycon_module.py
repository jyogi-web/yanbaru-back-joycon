from pyjoycon import JoyCon, get_R_id
import time
from datetime import datetime

def start_joycon_data_acquisition(joycon_data):
    score = 0  # 得点を初期化
    try:
        joycon_id = get_R_id()
        print(f"Joy-Con ID: {joycon_id}を取得しました。")

        joycon = JoyCon(*joycon_id)
        print("Joy-Conに接続しました。")

        prev_accel = {'x': 0, 'y': 0, 'z': 0}
        start_time = datetime.now()

        while True:
            try:
                status = joycon.get_status()
                accel = status['accel']
                print(f"取得した加速度データ: {accel}")

                accel_change = abs(accel['x'] - prev_accel['x'])

                if accel_change > 3000:
                    score += 10  
                    print(f"Joy-Conを振りました！得点: {score}")

                prev_accel = accel

                # Joy-Conデータを更新
                joycon_data["accel"] = accel
                joycon_data["score"] = score

                time.sleep(0.1)
                endtime = datetime.now()
                dlapsedtime = endtime - start_time 
                print("経過時間：", dlapsedtime)
            except Exception as e:
                print(f"データ取得中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"Joy-Con接続エラー: {e}")
