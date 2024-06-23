from flask import Flask, render_template

app = Flask(__name__)


# http://127.0.0.1:5000/index
@app.route("/index")
def index():
    # return "hello <h1>world</ h1>"
    return render_template("index.html")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run()
