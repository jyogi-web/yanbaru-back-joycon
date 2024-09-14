# Python生入れvarsion

## python 3.8.10のインストール

windowsinstaller(64-bit)
https://www.python.org/downloads/release/python-3810/

## ちゃんと入ったかチェック

```bash
py --version
```

`
Python 3.8.10
`

## PyJoycon関係のインストール

```bash
py -3.8 -m pip install joycon-python hidapi pyglm  
```

参考サイト
https://qiita.com/landwarrior/items/1b5e0f9af5316a025fe0

---

# 仮想環境varsion

## 仮想環境作成

プロジェクト直下に移動後、以下のコマンドを実行するとプロジェクト内に指定した仮想環境名のフォルダが作成されます。
venvと命名されることがよくあるので、迷ったらpython -m venv venvで大丈夫です。(コピペ)

```bash
python -m venv joycon
```

## 仮想環境立ち上げ

macの場合

```bash
. joycon/bin/activate
```

windowsの場合

```bash
.\joycon\Scripts\activate
```

## ライブラリインストール
ターミナルで(joycon) > みたいな感じになっているはずなのでそこで

```bash
pip install joycon-python hidapi pyglm flask
```

ちゃんと入ったか確認
```bash
pip list
```

結果

```
Package       Version
------------- ------------
hidapi        0.14.0.post2
joycon-python 0.2.4
pip           21.1.1
PyGLM         2.7.2
setuptools    56.0.0
```

ライブラリ関係書き出し
```bash
pip freeze > requirements.txt
```

コードの実行

```bash
python joycon.py
```

参考

https://qiita.com/shun_sakamoto/items/7944d0ac4d30edf91fde

### 記録
Rで記録が始まりZRで終了して、JSONを出すようにする
```
python ButtonGetInfo.py
```
### スコアを表示
フルとlocalhsot:5001にアクセスするとスコアが表示される

```
python app.py
```

