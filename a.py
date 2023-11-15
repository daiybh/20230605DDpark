from flask import Flask, jsonify


app = Flask(__name__)
# 指定浏览器渲染的文件类型，和解码格式
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


@app.route("/")
def index():
    data = {
        'key': '这是一个中文测试项'
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18086)