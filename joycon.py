from pyjoycon import JoyCon, get_R_id
import time
from datetime import datetime

# toDo
# - flaskに点数を反映
# - 曲のタイミングに合わせて振ることで点数化
# - 座標も判定の中に含める
# - 振動機能を使えるのか？
# - 

# pyjoyconの返り値
#  {
#   'battery': {
#     'charging': 0,
#     'level': 2
#   },
#   'buttons': {
#     'right': {
#       'y': 0,
#       'x': 0,
#       'b': 0,
#       'a': 0,
#       'sr': 0,
#       'sl': 0,
#       'r': 0,
#       'zr': 0
#     },
#     'shared': {
#       'minus': 0,
#       'plus': 0,
#       'r-stick': 0,
#       'l-stick': 0,
#       'home': 0,
#       'capture': 0,
#       'charging-grip': 0
#     },
#     'left': {
#       'down': 0,
#       'up': 0,
#       'right': 0,
#       'left': 0,
#       'sr': 0,
#       'sl': 0,
#       'l': 0,
#       'zl': 0
#     }
#   },
#   'analog-sticks': {
#     'left': {
#       'horizontal': 0,
#       'vertical': 0
#     },
#     'right': {
#       'horizontal': 2170,
#       'vertical': 1644
#     }
#   },
#   'accel': {
#     'x': 879,
#     'y': 1272,
#     'z': 549
#   },
#   'gyro': {
#     'x': -354,
#     'y': -7,
#     'z': 281
#   }
# }


# 得点を初期化
score = 0

try:
    # Joy-ConのIDを取得
    joycon_id = get_R_id()
    joycon = JoyCon(*joycon_id)

    # 前回の加速度データを保持する変数を用意
    prev_accel = {'x': 0, 'y': 0, 'z': 0}

    # 開始タイム取得
    start_time = datetime.now()

    while True:
        # Joy-Conのステータスを取得
        status = joycon.get_status()
        accel = status['accel']  # 加速度データ
        
        # 振る動作を検知 (例えばx軸方向の変化量が一定以上のとき)
        # !!!!!全ての軸で適応させる!!!!!
        accel_change = abs(accel['x'] - prev_accel['x'])

        # しきい値（ここでは50）を超えた場合に振ったとみなす
        if accel_change > 3000:
            score += 10  # 得点を加算
            print(f"Joy-Conを振りました！得点: {score}")

        # 現在の加速度データを前回のデータとして保存
        prev_accel = accel

        # ジャイロと加速度データを表示
        print("加速度:", accel)
        time.sleep(0.1)  # 0.1秒ごとにチェック
        endtime = datetime.now()
        dlapsedtime = endtime-start_time # 経過時間
        print("経過時間：",dlapsedtime)
except Exception as e:
    print(f"エラーが発生しました: {e}")
