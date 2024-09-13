from pyjoycon import GyroTrackingJoyCon, get_R_id
import time

# rotation(x 上下
# ,y左右
# ,z奥行
# )

joycon_id = get_R_id()
joycon = GyroTrackingJoyCon(*joycon_id)
while True:
    # print("joycon pointer:  ", joycon.pointer)
    print("joycon rotation: ", joycon.rotation)
    print("joycon direction:", joycon.direction)
    print("----------------------------")
    time.sleep(0.5)