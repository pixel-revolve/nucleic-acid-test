# nucleic-acid-test

本接口项目的技术选型：Python+Flask+MySQL+Redis，通过 Python+Flask 来开发接口，使用 MySQL 来存储用户信息，使用 Redis 用于存储 token，目前为纯后端接口，暂无前端界面，可通过 Postman、Jmeter、Fiddler 等工具访问请求接口。

## 项目部署

首先，下载项目源码后，在根目录下找到 requirements.txt 文件，然后通过 pip 工具安装 requirements.txt 依赖，执行命令：

```
pip3 install -r requirements.txt
```

接着将项目的数据库换成自己的数据库，在 config/setting.py 中修改对应的配置信息

修改完成后可以调用 static/sql/init.sql 进行数据库的初始化操作

接着，将项目部署起来，在本项目中其实就是利用 Python 执行 app.py 文件，以下为我在 Linux 上的部署命令。

```
# /root/nucleic-acid-test/app.py表示项目根路径下的app.py启动入口文件路径
# /root/nucleic-acid-test/nucleic-acid-test.log表示输出的日志文件路径
nohup python3 /root/nucleic-acid-test/app.py >/root/nucleic-acid-test/nucleic-acid-test.log 2>&1 &
```

## 接口文档

本项目集成了 flasgger,使用 SwaggerUI 展示接口文档
访问地址: http(s)://host:port/apidocs
推荐将 http(s)://host:port/nucleic-acid-test 作为 URL 导入 API 管理平台（Postman、ApiFox……）
