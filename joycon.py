from pyjoycon import JoyCon, get_R_id
import time

# 得点を初期化
score = 0

try:
    # Joy-ConのIDを取得
    joycon_id = get_R_id()
    joycon = JoyCon(*joycon_id)

    # 前回の加速度データを保持する変数を用意
    prev_accel = {'x': 0, 'y': 0, 'z': 0}

    while True:
        # Joy-Conのステータスを取得
        status = joycon.get_status()
        accel = status['accel']  # 加速度データ
        
        # 振る動作を検知 (例えばx軸方向の変化量が一定以上のとき)
        accel_change = abs(accel['x'] - prev_accel['x'])

        # しきい値（ここでは50）を超えた場合に振ったとみなす
        if accel_change > 7000:
            score += 10  # 得点を加算
            print(f"Joy-Conを振りました！得点: {score}")

        # 現在の加速度データを前回のデータとして保存
        prev_accel = accel

        # ジャイロと加速度データを表示
        print("加速度:", accel)
        time.sleep(0.1)  # 0.1秒ごとにチェック

except Exception as e:
    print(f"エラーが発生しました: {e}")
