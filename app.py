from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)
sql_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "db": "test",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}


# http://127.0.0.1:5000/index
@app.route("/index/")
def index():
    # return "hello <h1>world</ h1>"
    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # user = request.args.get("user")
        # age = request.args.get("age")
        # score = request.args.get("pwd")
        return render_template("login.html")
    elif request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        age = request.form.get("age")
        # 增（千万不要用字符串格式化容易被SQL注入比如format，应该用占位符）
        conn = pymysql.connect(**sql_config)
        cursor = conn.cursor()
        sql_str = "insert into dashboard_userinfo(name, password, age) values(%(name)s,  %(password)s, %(age)s)"
        cursor.execute(sql_str, {"name": user, "password": password, "age": int(age)})
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/user/list")
    return "界面异常"


@app.route("/user/list/")
def user_list():
    conn = pymysql.connect(**sql_config)
    cursor = conn.cursor()
    # 查
    sql_str = "select * from dashboard_userinfo"
    cursor.execute(sql_str)
    data_list = cursor.fetchall()
    print(data_list)
    cursor.close()
    conn.close()
    return render_template("user_list.html", title="传入的标题", data_list=data_list)


@app.route("/user/delete/")
def user_delete():
    nid = request.args.get("nid")
    # 删
    conn = pymysql.connect(**sql_config)
    cursor = conn.cursor()
    sql_str = "delete from dashboard_userinfo where id=%s"
    cursor.execute(sql_str, [nid])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/user/list")


@app.route("/user/change/")
def user_change():
    nid = request.args.get("nid")
    # 改
    conn = pymysql.connect(**sql_config)
    cursor = conn.cursor()
    sql_str = "update dashboard_userinfo set age=%s where id=%s"
    cursor.execute(sql_str, [0, nid])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/user/list")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run()
