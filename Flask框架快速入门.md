# Python Web Flask 框架

## 介绍

Flask 是一个轻量级的基于 Python 的 Web 框架。相较于 Django，更加轻量便捷，非常适合快速开发

## 安装

```shell
sudo pip install Flask
```

### 查看介绍和版本

```python
import flask
print(flask.__doc__)
print(flask.__version__)
```

## Hello World

### 项目结构

通过 Pycharm 新建一个 Flask 项目，可以看到初始化的目录结构为：

```bash
├─app.py
├─static
└─templates
```

- static 用于放置静态资源

- templates 存放模板文件

- app.py 是程序启动文件

### 第一个程序

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
```

运行结果：

```bash
FLASK_APP = app.py
FLASK_ENV = development
FLASK_DEBUG = 0
In folder C:/Users/Lin/Desktop/project/flask
"C:\Program Files\Python39\python.exe" -m flask run
 * Serving Flask app 'app.py' (lazy loading)
 * Environment: development
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [05/Jul/2022 20:39:10] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [05/Jul/2022 20:39:10] "GET /favicon.ico HTTP/1.1" 404 -
```

浏览器访问http://127.0.0.1:5000/就会显示Hello World

终端也会记录下访问的日志

```bash
127.0.0.1 - - [05/Jul/2022 20:39:10] "GET / HTTP/1.1" 200 -
```

### 修改 Flask 配置

```python
app = Flask(__name__)
```

其中，`__name__`为默认值`__main__`。可以将这个参数自定义为自己的项目名。也可以自定义静态资源、模板文件文件夹：

```python
app = Flask('my-project', static_folder='my-static', template_folder='my-template')
```

更多自定义参数可以进入源码查看

### Debug 模式

默认情况下，程序运行不会开启 debug 模式。此时，服务端出现错误信息不会在客户端显示。在开发过程中，查看错误信息是非常很有必要的，因此我们打开 debug 模式：

```python
app.run(debug=True)
```

另外，会触发热重载

### 绑定 IP 和端口

Flask 默认只能通过本机也就是`127.0.0.1`访问，默认端口为`5000`.

我们可以自定义：

```python
app.run(host='0.0.0.0', port=8080, debug=True) # 0.0.0.0 代表所有网卡可以访问
```

## 获取 URL 参数

URL 参数即出现在 url 中的键值对，例如http://127.0.0.1?username=jay-chou&password=123456

则此时的参数是

```json
{
  "username": "jay-chou",
  "password": "123456"
}
```

可以通过以下示例程序查看

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return request.args.__str__()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

则会在网页上显示

```bash
ImmutableMultiDict([('username', 'jay-chou'), ('password', '123456')])
```

`request`方法还有多个 API，这里简单罗列一下

可以通过一下程序进行测试体会

```python
from importlib.resources import path
from flask import Flask, request
from sympy import re

app = Flask(__name__)

@app.route('/')
def hello_world():
    path = request.path  # 获取装饰器下的路径
    full_path = request.full_path  # 获取完整路径带上参数信息
    username = request.args.get('username')  # 获取指定键值
    # 同上 第二个参数表示默认值，当第一个参数获取的值为None时，则取默认值
    password = request.args.get('password', 'default')
    list = request.args.getlist('p')  # 获取同一个键的所有值，以列表的方式存下来
    print('===================')
    print(path)
    print(full_path)
    print(username)
    print(password)
    print(list)
    print('===================')
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
```

控制台输出结果：

```bash
===================
/
/?username=jay-chou&p=1&p=2
jay-chou
default
['1', '2']
===================
```

## 获取 POST 参数

在实际开发中，我们遵行 RESTFUL 风格，一般数据都通过表单提交，使用 POST 请求，一下示例程序将简单展示如何获取 POST 表单

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/login', methods=['POST']) # 限制只能通过POST请求来访问该API
def login():
    print('=============================')
    print(request.headers)  # 获取HTTP请求头
    print(request.stream.read())  # 流式读取请求数据
    print('=============================')
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

这里我使用`ApiFox`进行测试：

![image-20220706102834115](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706102834115.png)

控制台打印结果：

```bash
=============================
User-Agent: apifox/1.0.0 (https://www.apifox.cn)
Content-Type: application/json
Accept: */*
Host: 127.0.0.1
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 57


b'{\r\n    "username":"Jay-Chou",\r\n    "password":"123456"\r\n}'
=============================
```

可以看到我们获取到的是二进制数据，此时，我们可以使用 Flask 自带的表单解析 API

```python
@app.route('/login', methods=['POST'])
def login():
    print('=============================')
    print(request.headers)
    print(request.form)
    print(request.form['username'])
    print(request.form['password'])
    print('=============================')
    return 'OK'
```

![image-20220706103627152](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706103627152.png)

```bash
=============================
User-Agent: apifox/1.0.0 (https://www.apifox.cn)
Accept: */*
Host: 127.0.0.1
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 33


ImmutableMultiDict([('username', 'Jay-Chou'), ('password', '123456')])
Jay-Chou
123456
=============================
```

注意此时`Content-Type`为`application/x-www-form-urlencoded`

## 解析 JSON

大多数情况下，前后端交互都是通过 JSON 的方式，`Content-Type`此时为`application/json`， 那么我们应该将其解析成对应的 Python 类型

```python
@app.route('/login', methods=['POST'])
def login():
    print('=============================')
    print(request.headers)
    print(request.json)
    print(request.json['username'])
    print(request.json['password'])
    print(type(request.json))
    print('=============================')
    return 'OK'
```

![image-20220706104143150](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706104143150.png)

控制台打印结果：

```bash
=============================
User-Agent: apifox/1.0.0 (https://www.apifox.cn)
Content-Type: application/json
Accept: */*
Host: 127.0.0.1
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 57


{'username': 'Jay-Chou', 'password': '123456'}
Jay-Chou
123456
<class 'dict'>
=============================
```

### 返回体自定义

#### 方式一

```python
@app.route('/login', methods=['POST'])
def login():
    res = request.json
    # 方式一
    resp = Response(json.dumps(res), mimetype='application/json')
    return resp
```

#### 方式二

```python
@app.route('/login', methods=['POST'])
def login():
    res = request.json
    # 方式一
    resp = jsonify(res)
    return resp
```

均会得到返回结果：

```json
{
  "password": "123456",
  "username": "Jay-Chou"
}
```

## 上传文件

上传文件也是使用 POST 方法，这里我们将上传的文件放在`static`目录下

示例程序

```python
from uuid import uuid1
from flask import Flask, request
import os

app = Flask(__name__)

# 文件上传目录
app.config['UPLOAD_FOLDER'] = 'static'
# 支持的文件格式
app.config['ALLOW_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


def isAllowed(filename):  # 判断是否为指定格式
    # rsplit方法表示从字符串后面开始分割，第二个参数表示分割次数
    # 例如：xxx.png.jpg 会被分割为 ['xxx.png','jpg']
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOW_EXTENSIONS']


def generateName(filename):
    return str(uuid1()) + '.' + filename.rsplit('.', 1)[1]


@app.route('/upload', methods=['POST'])
def upload():
    try:
        image = request.files['image']
        if image and isAllowed(image.filename):
            # 使用自定义文件名保存图片（这里采用UUID）
            filename = generateName(image.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(path)
            image.save(path)
            return 'success'
        else:
            return 'fail'
    except Exception as e:
        print(e)
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

使用`ApiFox`进行测试：
![image-20220706151536714](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706151536714.png)
![image-20220706151526649](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706151526649.png)

## RESTFUL 风格 URL

### 初探

采用 restful 风格的 url 可以取代原始的方式

下面是示例程序：

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/user/<username>')
def queryUser(username):
    print(username)
    print(type(username))
    return 'welcome ' + username


@app.route('/user/<username>/all')
def queryAllUsers(username):
    print(username)
    print(type(username))
    return 'welcome ' + username


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

- 访问http://127.0.0.1/user/jay-chou

  - 返回 welcome jay-chou
  - 打印

  ```bash
  jay-chou
  <class 'str'>
  ```

- 访问http://127.0.0.1/user/jay-chou/

  - 返回 Not Found

- 访问http://127.0.0.1/user/jay-chou//all

  - 返回 welcome jay-chou
  - 打印

  ```bash
  jay-chou
  <class 'str'>
  ```

  由此可以看出，传递的都是 str 类型的变量，且 url 必须完整

### 类型转换

如果需求是根据用户 ID 查询，那么我们就要拿到一个数字类型的变量，此时可以这么做：

```python
@app.route('/user/queryById/<int:num>')
def queryUserById(num):
    print(num)
    print(type(num))
    return '查询成功'
```

若访问http://127.0.0.1/user/queryById/1

则会返回`查询成功`，打印

```bash
1
<class 'int'>
```

若 url 中不是一个数字，则会返回 Not Found
![image-20220706153708150](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706153708150.png)

Flask 自带的转换器类型：

- int 接受整数
- float 接受浮点数
- string 默认是字符串接收器
- path 和默认相似 但也接受斜线

此外，可以自定义转换器用于校验，这里就不多赘述了

### 使用 url_for

工具函数`url_for`可以让你以软编码的形式生成 url，提供开发效率

```python
from flask import Flask, request, url_for

app = Flask(__name__)


@app.route('/user/<path:username>')
def queryUser(username):
    print(username)
    print(type(username))
    return 'welcome ' + username


@app.route('/user/<username>/all')
def queryAllUsers(username):
    print(username)
    print(type(username))
    return 'welcome ' + username


@app.route('/user/queryById/<int:num>')
def queryUserById(num):
    print(num)
    print(type(num))
    return '查询成功'


@app.route('/test')
def test():
    print(url_for('queryUser', username='jay-chou'))
    print(url_for('queryAllUsers', username='jay-chou'))
    print(url_for('queryUserById', num='666'))
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

打印结果：

```bash
/user/jay-chou
/user/jay-chou/all
/user/queryById/666
```

## redirect 重定向

使用 redirect 方法，前端对执行重定向

```python
from flask import Flask, request, redirect

app = Flask(__name__)


@app.route('/redirect')
def my_redirect():
    return redirect('https://www.bilibili.com')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

## 使用 jinja2 模板引擎

```python
from flask import Flask, abort, render_template, request, redirect

app = Flask(__name__)


@app.route('/index/<username>')
def index(username):
    return render_template('index.html', username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

```

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <h1>welcome: {{username}}</h1>
  </body>
</html>
```

访问http://127.0.0.1/index/jay-chou

![image-20220706161252973](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220706161252973.png)

可以看到，网页被渲染了出来

## 连接数据库

### 引入库

```bash
pip install pymysql
```

### 规范一个数据库操作类（以 MySQL 为例）

```python
class MysqlDb():

    def __init__(self, host, port, user, passwd, db):
        # 建立数据库连接
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            autocommit=True
        )
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            print("操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()
```

### 实例化一个全局单例

```python
db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB)
```

相关数据库配置信息自行配置

### 全局使用

在开发代码中，写好需要使用的 SQL 语句，调用全局单例 db 提供的 API，执行数据库事务

举一个例子，首先新建一个用户表：

```sql
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nick_name` varchar(255) NOT NULL,
  `age` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

插入几个数据

```sql
INSERT INTO `user` VALUES (1, '小明', 5);
INSERT INTO `user` VALUES (2, '小红', 18);
```

这里我们获取用户表中所有的用户信息：

```python
sql = 'select * from user'
data = db.select_db(sql)
print(data)
```

打印结果：

```bash
[{'id': 1, 'nick_name': '小明', 'age': 5}, {'id': 2, 'nick_name': '小红', 'age': 18}]
```

笔者也浅尝过 Flask 的 ORM 框架，但说实话，并没有简单操作，甚至有些复杂……因此，这里就不做阐述了

## 自定义装饰器

### 导包

```python
from functools import wraps
```

### 自定义处理逻辑

```python
from flask import Flask, abort
from functools import wraps

app = Flask(__name__)


def has_powercode(powercode):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """处理逻辑（简化处理）"""
            if powercode != 'user:add':
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/api/user/add', methods=['GET'])
@has_powercode('user:delete')
def add_user():
    return 'success'


if __name__ == '__main__':
    app.run()

```

网页简单测试一下：

![image-20220708224340905](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220708224340905.png)

很遗憾，在装饰器因权限不足，出发了 abort(403)，程序就不会结束该函数，不会继续执行被该装饰器所修饰的函数了

### 能做些什么

我们可以用来做`Authentication`和`Authorization`(可恶，想起了无聊的搬砖生活……)

通过装饰器，自定义个性化的身份验证和鉴权逻辑，从而满足系统的安全保障

## 配置 Swagger 文档

作为一个开发工程师，写好一个接口文档在团队协作中非常重要，Flask 也集成了 Swagger 文档，我们来看看怎么使用

### 引入库

```bash
pip install flasgger
```

### 配置相关信息

```python
from flasgger import Swagger

swagger_config = Swagger.DEFAULT_CONFIG  # Swagger通过配置信息渲染SwaggerUI展示信息
swagger_config['title'] = TITLE  # 接口文档标题
swagger_config['version'] = VERSION  # 版本号
swagger_config['termsOfService'] = TERMSOFSERVICE  # 条文说明
swagger_config['specs'][0]['route'] = ROUTE  # 接口集合路由
swagger_config['description'] = DESCRIPTION  # 描述

Swagger(app, config=swagger_config)
```

### 对应每一个接口填写描述信息

例如，我们这里有一个通过用户名称获取用户信息的接口：

```python
@app.route('/api/user/queryByName/<string:username>', methods=["GET"])
def queryUserByName(username):
    """
    通过名称获取用户信息
    ---
    tags:
      - 用户接口
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: 用户名称
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到该用户
      0:
        description: 查询成功
    """
    return user.queryByName(username)
```

相关描述信息以 yaml 的形式写在了方法下面的注释代码块里面（个人觉得很魔性）

flasgger 包里会有程序来阅读这些配置，并将描述信息渲染在页面上

### 真实的样貌

![image-20220708222333577](https://0-bit.oss-cn-beijing.aliyuncs.com/image-20220708222333577.png)

## 开启跨域

### 引入库

```shell
pip install flask-cors
```

### 常用配置

```python
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
```
