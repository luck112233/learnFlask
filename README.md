# Flask

## 创建项目

- 本地安装flask库：python -m pip install flask
- pycharm创建项目选择本地解释器
- 新建main.py

```{.html}
from flask import Flask, render_template

app = Flask(__name__)


# http://127.0.0.1:5000/show/info
@app.route("/show/info")
def index():
    # return "hello <h1>world</ h1>"
    # index.html在templates文件夹下
    return render_template("index.html")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run()
```

- 打开pycharm终端运行pip install flask
- 根目录新建learn_web.py

```{.py}
# -*- coding: UTF-8 -*
# templates文件夹存放html文件
# static文件夹存放图片
from flask import Flask, render_template  # pip install flask
import pymysql # pip install pymysql

# 新建app类
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

# 创建了网址 /show/info 和函数index的对应关系
@app.route("/show/info")
def index():
    # 读取文本的字符串并返回
    # return "内容"
    # 连接mysql
    conn = pymysql.connect(**sql_config)
    cursor = conn.cursor()
    # 查
    sql_str = "select * from tb1"
    cursor.execute(sql_str)
    data_list = cursor.fetchall()
    print(data_list)
    # 关闭
    cursor.close()
    conn.close()
    return render_template("index.html", title="传入的标题", data_list=data_list)

@app.route("/show/more")
def show_more():
    return "<h1>标题</h1>返回简单字符串"

if __name__ == '__main__':
    app.run()
```

- get请求：向后台传入的数据会拼接在url上，数据之间用&,网址和数据之间用?
- post请求：提交的数据不在url中而是在请求体中

```{.py}
# 只能通过get方式调用
@app.route("/get/reg", methods=["GET"])
def get_reg():
    # 读取文本的字符串并返回
    print(request.args.get("user"))
    print(request.args.get("pwd"))
    return "注册成功"


# 只能通过post方式调用
@app.route("/post/reg", methods=["POST"])
def post_reg():
    # 读取文本的字符串并返回
    print(request.form.get("user"))
    print(request.form.get("pwd"))
    return "注册成功"


# get或者post方式调用
@app.route("/reg", methods=["GET", "POST"])
def reg():
    user = ""
    pwd = ""
    age = ""
    # 连接mysql
    conn = pymysql.connect(**sql_config)
    cursor = conn.cursor()

    if request.method == "GET":
        user = request.args.get("user")
        pwd = request.args.get("pwd")
        age = request.args.get("age")
        # 增（千万不要用字符串格式化容易被SQL注入比如format，应该用占位符）
        sql_str = "insert into tb1(name, age) values(%(name)s, %(age)s)"
        cursor.execute(sql_str, {"name": user, "age": int(age)})
        conn.commit()
    elif request.method == "POST":
        user = request.form.get("user")
        pwd = request.form.get("pwd")
        age = request.form.get("age")
        # 删
        sql_str = "delete from tb1 where id=%s"
        cursor.execute(sql_str, [1])
        conn.commit()
        # 改
        sql_str = "update tb1 set score=%d where id=%s"
        cursor.execute(sql_str, [0, 1])
        conn.commit()
    # 关闭
    cursor.close()
    conn.close()
    return "添加成功"
```

```{.html}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!-- form标签包裹数据，里面定义提交方式，提交地址 -->
    <!-- 必须包含一个submit, 一定要有那么属性 -->
    <form method="get" action="/get/reg">
        用户名: <input type="text" name="user" />
        密码: <input type="password" name="pwd" />
        <input type="submit" value="get提交表单">
    </form>

    <form method="get" action="/reg">
        <input type="text" name="user" placeholder="用户名">
        <input type="text" name="pwd" placeholder="密码">
        <input type="text" name="age" placeholder="年龄">
        <input type="submit" value="提交表单">
    </form>

    <h1>{{title}}</h1>
    <table>
        <thead>
            <th>ID</th>
            <th>用户名</th>
            <th>年龄</th>
        </thead>
        <tbody>
        {% for item in data_list %}
            <tr>
                <td>{{ item.id }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.age }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    </table>
</body>
</html>
```
