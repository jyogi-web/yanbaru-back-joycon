from flask import Flask
from joycon import joycon

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# ↓ /scrapingをGETメソッドで受け取った時の処理
@app.route('/joycon')
def get():
    print("joycon")
    # ↓　実行したいファイルの関数
    return joycon.Joycon()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
