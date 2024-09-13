


## Dockerコンテナのビルドと実行
Docker Composeを使用して、コンテナをビルドしてバックグラウンドで実行します：
```
docker-compose up -d --build

```

`http://localhost:5001/`にアクセス

コンテナを停止するには、次のコマンドを使用します：
```
docker-compose down
```

## 必要なライブラリの追加
追加のPythonライブラリをインストールする場合は、`requirements.txt`ファイルにライブラリ名を追加します。


---

---
title: 【Python】Pygame で Nintendo Switch の Joy-Con(L) の操作を検出
tags: Python pygame Nintendo Joy-Con
author: Kazuhito
slide: false
---
ロボット開発のデバッグにコントローラーを使いたくて、何か良いの無いかと探しておりました。

はじめは、[iBUFFALO USBゲームパッド SFC風](https://www.amazon.co.jp/iBUFFALO-USB%E3%82%B2%E3%83%BC%E3%83%A0%E3%83%91%E3%83%83%E3%83%89-8%E3%83%9C%E3%82%BF%E3%83%B3-%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%83%95%E3%82%A1%E3%83%9F%E3%82%B3%E3%83%B3%E9%A2%A8-BSGP801GY/dp/B002B9XB0E) とか良いかなと考えていたのですが、
Joy-ConがBluetooth接続で簡単に使用できると聞いて、Joy-Conへ方向転換。
PythonのPygameを用いて簡単に検出できたので、手順を以下にメモ。

① Joy-ConをBluetooth接続モードへ移行
![01.png](https://qiita-image-store.s3.amazonaws.com/0/140207/afa0082d-0d11-f972-8072-5e32c8561984.png)

②-1 Windows側でBluetooth機器を検出
![2017-12-05 (16).png](https://qiita-image-store.s3.amazonaws.com/0/140207/af5b58ab-8fc4-5d4f-344c-64edbcf46481.png)
②-2 Windows側でBluetooth機器を検出
![2017-12-05 (17).png](https://qiita-image-store.s3.amazonaws.com/0/140207/1acc80d1-1f21-10b9-5047-efdb2b765296.png)
②-3 Windows側でBluetooth機器を検出
![2017-12-05 (18).png](https://qiita-image-store.s3.amazonaws.com/0/140207/7d2c4e5d-dd13-ae9f-2ae6-38a3ed398127.png)
②-4 Windows側でBluetooth機器を検出
![2017-12-05 (19).png](https://qiita-image-store.s3.amazonaws.com/0/140207/2a24796a-3385-2249-04ca-98b6a5b5acf0.png)
②-5 Windows側でBluetooth機器を検出
![2017-12-05 (20).png](https://qiita-image-store.s3.amazonaws.com/0/140207/b1514296-282e-8360-c91b-2cbcb1057781.png)




実際に検出してみたところの動画は以下。
https://www.youtube.com/watch?v=UiDuYm2suMk
[![【Python】Nintendo Switch の JOY-CON を Pygame で Joy-Con の操作を検出
](https://img.youtube.com/vi/UiDuYm2suMk/0.jpg)](https://www.youtube.com/watch?v=UiDuYm2suMk)

スティックは、ハットスイッチとして検出するようで、以下のような割り付けになっておりました(横向き持ちの場合)
　スティック左倒し：ハットスイッチ X軸 -1
　スティック右倒し：ハットスイッチ X軸 1
　スティック上倒し：ハットスイッチ Y軸 1
　スティック下倒し：ハットスイッチ Y軸 -1
　SL：ボタン 4
　SR：ボタン 5
　L ：ボタン 14
　ZL：ボタン 15
　十字キー 左：ボタン 2
　十字キー 右：ボタン 1
　十字キー 上：ボタン 3
　十字キー 下：ボタン 0
　- ：ボタン 8
　キャプチャーボタン ：ボタン 13

　モーションIRカメラ、NFC、加速度センサー、ジャイロセンサーとかスティックの微妙な倒し具合 は検出できない模様。
HD振動とか指示出来たら、色々楽しめそうですが、今のところ操作出来るか不明。

ソースコードは以下。

```py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import time

def main() :
    pygame.joystick.init()
    joystick0 = pygame.joystick.Joystick(0)
    joystick0.init()
    
    print 'joystick start'
    
    pygame.init()

    while True:
         # コントローラーの操作を取得
        eventlist = pygame.event.get()

        # イベント処理
        for e in eventlist:
            if e.type == QUIT:
                return

            if e.type == pygame.locals.JOYAXISMOTION:
                x, y = joystick0.get_axis(0), joystick0.get_axis(1)
                print 'axis x:' + str(x) + ' axis y:' + str(y)
            elif e.type == pygame.locals.JOYHATMOTION:
                x, y = joystick0.get_hat(0)
                print 'hat x:' + str(x) + ' hat y:' + str(y)
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                print 'button:' + str(e.button)

        time.sleep(0.1)
 
if __name__ == '__main__':
    try:
        main()
    except pygame.error:
        print 'joystickが見つかりませんでした。'

```

以上。

---

---
title: Joy-ConにPythonからBluetooth接続をして6軸センサーと入力情報を取得する
tags: Joy-Con NintendoSwitch Python bluetooth HID
author: tocoteron
slide: false
---
# はじめに
ィヤッフゥウ〜〜〜↑↑↑！こんにちは、配管工始めました。トコロテンです。
この記事では、[Nintendo Switch](https://www.nintendo.co.jp/hardware/switch/)のジョイコン(Joy-Con)をPython3から接続して6軸センサーを含む各種入力を取得する方法を紹介します。

以下のリポジトリにてJoy-Conのプチドライバ(?)の実装を公開しています。まだ開発を始めたばかりですがよければ開発に協力していただけると嬉しいです。ドキュメントを近いうちに整備して機能も増やしていく予定です。
https://github.com/tokoroten-lab/joycon-python

# 動作環境
以下の環境で動作を確認しました。

- macOS Mojave (10.14.6)
- Python (3.7.4)
    - hidapi (0.7.99.post21)

# Joy-Conの仕様
Joy-Conの主な仕様や各種名称は任天堂の以下の公式サイトで確認することができます。
https://www.nintendo.co.jp/hardware/switch/feature/index.html#3
また、以下のリポジトリでJoy-Conの仕様をリバースエンジニアリングを用いて解析した情報が公開されています。かなり詳しい仕様が載っているため、1度目を通しておくことをおすすめします。この記事を書くにあたって大変お世話になりました。ありがとうございます。
https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering

# Joy-Conとの通信

## Bluetooth/HIDで接続する

### 仕様確認
Joy-Conとの通信にはBluetooth/HIDを用いて接続することが可能です。
HIDのInput, Output, Featureレポートのフォーマットは以下のページにて確認できます。
https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md

### サンプルプログラム

#### 準備
PythonでBluetooth/HIDを用いた接続を利用するためには[cython-hidapi](https://github.com/trezor/cython-hidapi)を利用しました。以下のようにして`pip`でインストールが可能です。

```bash
sudo pip install hidapi
```

##### 注意点
@shksさんの[python モジュールhidapiとhidに注意。](https://qiita.com/shks/items/c311f736cf42742349e6)という記事にあるように、`hidapi`に似たライブラリで`hid`といったものがあります。間違えないように気をつけましょう。プログラム内でimportする際にはどちらも`import hid`となります。

#### ペアリング確認用プログラム
以下のプログラムを実行することで認識しているHIDデバイス一覧を取得できます。
この中にJoy-Conの情報があるか確認してみましょう。無い場合はJoy-Conと端末がペアリングされていないため、ペアリングしてからもう一度実行してみてください。

```Python3:devices_list.py
import hid

for device in hid.enumerate(0, 0):
    for k, v in device.items():
        print ('{} : {}'.format(k, v))
    print ('')
```

私の環境では以下のようなセクションが表示されました。`product_string : Joy-Con (L)`といった表記からこれがJoy-Conのデバイス情報であることがわかります。また、`vendor_id`と`product_id`が[USB ID Database](https://www.the-sz.com/products/usbid/index.php?v=&p=&n=Joy-Con)にて調べた情報と一致していることからもわかります。

```
path : b'IOService:/IOResources/IOBluetoothHCIController/AppleBroadcomBluetoothHostController/IOBluetoothDevice/IO
BluetoothL2CAPChannel/IOBluetoothHIDDriver'
vendor_id : 1406
product_id : 8198
serial_number : b8-78-26-46-9b-84
release_number : 1
manufacturer_string : Unknown
product_string : Joy-Con (L)
usage_page : 1
usage : 5
interface_number : -1
```

#### ボタンデータ取得用プログラム

Joy-ConのVendor IDとProduct IDは以下の通りです。この情報を利用して接続をします。

- Joy-Con (L)
    - Vendor ID : 0x057E(1406)
    - Product ID: 0x2006(8198)

- Joy-Con (R)
    - Vendor ID : 0x057E(1406)
    - Product ID: 0x2007(8199)

また、Joy-ConのHIDのInputレポートのフォーマットは以下のページの通りです。
https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md#input-reports
試しにJoy-Conのボタンやスティックの入力情報を取得してみましょう。
これに対応するInputレポートは[INPUT 0x3F](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md#input-0x3f)です。
このInputレポートを受け取るためには、まず[OUTPUT 0x01](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md#output-0x01)のフォーマットに従って[Subcommand 0x03](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_subcommands_notes.md#subcommand-0x03-set-input-report-mode)のサブコマンドを送信します。このサブコマンドには引数が存在し、`0x3F`を指定することでJoy-Conのボタンの入力状態の変化があったときのみ`INPUT 0x3F`のInputレポートを発行するようになります。レポートのサイズは12バイトです。
*実はJoy-Conは初期状態でInputレポート`INPUT 0x3F`を送信するようになっていますが、ここではあえて設定します。なぜなら、Joy-ConのInputレポートの前回の設定が引き継がれている可能性があるためです。*

```Python3:joycon_read_test.py
import hid
import time

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

if __name__ == '__main__':

    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)

    write_output_report(joycon_device, 0, b'\x01', b'\x03', b'\x3f')

    while True:
        print(joycon_device.read(12))
```

Joy-Conと端末をペアリングした状態で上のプログラムを実行してJoy-Conで何か操作をするとInputレポートの情報が標準出力に出力されます。
`write_output_report(...)`メソッドにてOutputレポートを構築して送信します。
引数の`packet_number`はレポートを送るごとに0x0-0xFの範囲でインクリメントする必要があります。

#### プレイヤーランプ操作用プログラム
ここではJoy-Conのプレイヤーランプを用いて簡単な2進4ビットカウンタを動作させる方法を紹介します。先ほどと同じ要領で`OUTPUT 0x01`レポートを送信します。サブコマンドは[Subcommand 0x30](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_subcommands_notes.md#subcommand-0x30-set-player-lights)を用います。また、ランプの点灯・点滅パターンを1Byteで引数として設定します。

##### ビット解釈
ランプの点灯・点滅パターンは各4bitずつ合わせて1Byteで表現します。
上位4bitが点滅パターンで下位4bitが点灯パターンです。
ビットが0であるとき消灯を意味し、1である場合には点灯・点滅を意味します。

従って、全点灯や全点滅に対応したビット列は以下のようになります。

- 全点灯: 0b00001111
- 全点滅: 0b11110000

では、以下のようなビット列はどのような結果を得られるでしょうか。

- 0b00010001

点灯・点滅で同じ位置に対応するビットが1になっています。このような場合には、点灯が優先されます。したがって、あるランプが点滅する条件は、対応する点滅用のビットが1であり点灯用のビットが0であることが条件です。

以上を踏まえて4bit(Joy-Conのプレイヤーランプは4個)のアップカウンタを実装してみます。

##### 点灯バージョン

```Python3:joycon_player_lamp.py
import hid
import time

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

if __name__ == '__main__':

    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)

    count = 0
    while True:
        time.sleep(1)
        write_output_report(joycon_device, count, b'\x01', b'\x30', count.to_bytes(1, byteorder='big'))
        count = (count + 1) & 0xf
```

##### 点滅バージョン

```Python3:joycon_player_lamp.py
import hid
import time

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

if __name__ == '__main__':

    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)

    count = 0
    while True:
        time.sleep(1)
        write_output_report(joycon_device, count, b'\x01', b'\x30', (count << 4).to_bytes(1, byteorder='big'))
        count = (count + 1) & 0xf
```

プレイヤーランプを点灯・点滅させることができました。[Subcommand 0x38](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_subcommands_notes.md#subcommand-0x30-set-player-lights)を利用することでHOMEボタンを光らせることもできるようです。興味のある方はぜひやってみてください。

#### ボタン&スティック&6軸センサーデータ取得用プログラム
Joy-ConにはボタンやXYZ軸の加速度センサーとジャイロセンサーが搭載されています。
これらのデータを取得するためには、まずセンサーを有効化した後にInputレポートの形式を変える必要があります。
まず、`OUTPUT 0x01`で[Subcommand 0x40](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_subcommands_notes.md#subcommand-0x40-enable-imu-6-axis-sensor)に引数として`1`を与えると各センサーが有効化されます。次に、`OUTPUT 0x01`で[Subcommand 0x03](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_subcommands_notes.md#subcommand-0x03-set-input-report-mode)に引数として`0x30`を与えると60Hzでボタン、スティック、6軸センサーの全てのデータを定期的に送信するようになります。

##### データ取得のみ

```Python3:joycon_sensors.py
import hid
import time

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

if __name__ == '__main__':

    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)

    # 6軸センサーを有効化
    write_output_report(joycon_device, 0, b'\x01', b'\x40', b'\x01')
    # 設定を反映するためには時間間隔が必要
    time.sleep(0.02)
    # 60HzでJoy-Conの各データを取得するための設定
    write_output_report(joycon_device, 1, b'\x01', b'\x03', b'\x30')

    while True:
        print(joycon_device.read(49))
```

各データをバイト列として取得しただけではどうしようもないので実際に扱えるデータにデコードしてみましょう。

##### データ取得&デコード

全体のデータフォーマットは[Standard input report format](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md#standard-input-report-format)にて確認できます。6軸センサーのデータフォーマットは[6-Axis sensor information](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/imu_sensor_notes.md)にて確認できます。ドキュメント中にある`Int16LE`といった表記は符号付き16ビット整数でバイトオーダーが**リトルエンディアン**(一般的なバイトの並び方と逆)であることを意味しています。
また、加速度センサーから取得したデータには[オフセット](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/spi_flash_notes.md#6-axis-horizontal-offsets)が加算されています。基準値を0にした方が扱いやすいため、このオフセット分を考慮してデコードを行う必要があります。
これらのことを考慮してデータの一部をデコードするプログラムの実装例を以下に示します。

```Python3:a
import hid
import time

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

L_ACCEL_OFFSET_X = 350
L_ACCEL_OFFSET_Y = 0
L_ACCEL_OFFSET_Z = 4081
R_ACCEL_OFFSET_X = 350
R_ACCEL_OFFSET_Y = 0
R_ACCEL_OFFSET_Z = -4081

MY_PRODUCT_ID = L_PRODUCT_ID

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

def is_left():
    return MY_PRODUCT_ID == L_PRODUCT_ID

def to_int16le_from_2bytes(hbytebe, lbytebe):
    uint16le = (lbytebe << 8) | hbytebe 
    int16le = uint16le if uint16le < 32768 else uint16le - 65536
    return int16le

def get_nbit_from_input_report(input_report, offset_byte, offset_bit, nbit):
    return (input_report[offset_byte] >> offset_bit) & ((1 << nbit) - 1)

def get_button_down(input_report):
    return get_nbit_from_input_report(input_report, 5, 0, 1)

def get_button_up(input_report):
    return get_nbit_from_input_report(input_report, 5, 1, 1)

def get_button_right(input_report):
    return get_nbit_from_input_report(input_report, 5, 2, 1)

def get_button_left(input_report):
    return get_nbit_from_input_report(input_report, 5, 3, 1)

def get_stick_left_horizontal(input_report):
    return get_nbit_from_input_report(input_report, 6, 0, 8) | (get_nbit_from_input_report(input_report, 7, 0, 4) << 8)

def get_stick_left_vertical(input_report):
    return get_nbit_from_input_report(input_report, 7, 4, 4) | (get_nbit_from_input_report(input_report, 8, 0, 8) << 4)

def get_stick_right_horizontal(input_report):
    return get_nbit_from_input_report(input_report, 9, 0, 8) | (get_nbit_from_input_report(input_report, 10, 0, 4) << 8)

def get_stick_right_vertical(input_report):
    return get_nbit_from_input_report(input_report, 10, 4, 4) | (get_nbit_from_input_report(input_report, 11, 0, 8) << 4)

def get_accel_x(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 13 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 14 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_X if is_left() else R_ACCEL_OFFSET_X))

def get_accel_y(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 15 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 16 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_Y if is_left() else R_ACCEL_OFFSET_Y))

def get_accel_z(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 17 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 18 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_Z if is_left() else R_ACCEL_OFFSET_Z))

def get_gyro_x(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 19 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 20 + sample_idx * 12, 0, 8))

def get_gyro_y(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 21 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 22 + sample_idx * 12, 0, 8))

def get_gyro_z(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 23 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 24 + sample_idx * 12, 0, 8))

if __name__ == '__main__':

    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, MY_PRODUCT_ID)

    # 6軸センサーを有効化
    write_output_report(joycon_device, 0, b'\x01', b'\x40', b'\x01')
    # 設定を反映するためには時間間隔が必要
    time.sleep(0.02)
    # 60HzでJoy-Conの各データを取得するための設定
    write_output_report(joycon_device, 1, b'\x01', b'\x03', b'\x30')

    while True:
        input_report = joycon_device.read(49)
        # ボタン
        print("Button: {} {} {} {}".format("DOWN "  if get_button_down(input_report) else "",
                                           "UP "    if get_button_up(input_report) else "",
                                           "RIGHT " if get_button_right(input_report) else "",
                                           "LEFT "  if get_button_left(input_report) else ""))
        # アナログスティック
        print("Stick : {:8d} {:8d}".format(get_stick_left_horizontal(input_report),
                                           get_stick_left_vertical(input_report)))
        # 加速度センサー
        print("Accel : {:8d} {:8d} {:8d}".format(get_accel_x(input_report),
                                                 get_accel_y(input_report),
                                                 get_accel_z(input_report)))
        # ジャイロセンサー
        print("Gyro  : {:8d} {:8d} {:8d}".format(get_gyro_x(input_report),
                                                 get_gyro_y(input_report),
                                                 get_gyro_z(input_report)))
        print()
```

### まとめ
[dekuNukemさんのリポジトリ](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering)を見れば今回紹介したことよりも多くのことができるようになります。しかし、まだ解析されていない部分もいくつかあります。有識者の方がいたら教えていただけると嬉しいです。
