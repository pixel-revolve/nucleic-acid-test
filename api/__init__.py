from flask import Flask, jsonify, render_template, request
import api.manufacturer as manufacturer
import api.manufacturer_detection_box as manufacturer_detection_box
import api.qr_code as qr_code
import api.upload as upload
import api.watermark as watermark
import api.user as user
import api.covid_detect as covid_detect
from flasgger import Swagger
from flask_cors import CORS
from common.check import detect

from config.setting import DESCRIPTION, ROUTE, TERMSOFSERVICE, TITLE, VERSION

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示


swagger_config = Swagger.DEFAULT_CONFIG  # Swagger通过配置信息渲染SwaggerUI展示信息
swagger_config['title'] = TITLE  # 接口文档标题
swagger_config['version'] = VERSION  # 版本号
swagger_config['termsOfService'] = TERMSOFSERVICE  # 条文说明
swagger_config['specs'][0]['route'] = ROUTE  # 接口集合路由
swagger_config['description'] = DESCRIPTION  # 描述

Swagger(app, config=swagger_config)


"""
协议说明
"""


@app.route('/terms')
def terms():
    return render_template('terms.html')


"""
下面为生产厂商相关路由注册
"""


@app.route(manufacturer.baseUrl + "/addManufacturer", methods=["POST"])
def add_manufacturer():
    """
    添加生产商
    ---
    tags:
      - 生产商接口
    responses:
      1001:
        description: 不可传入空
      1002:
        description: 该厂商已经存在
      1003:
        description: 该厂商前缀已经存在
      0:
        description: 恭喜，添加成功
    """
    return manufacturer.add_manufacturer()


@app.route(manufacturer.baseUrl + "/manufacturerDelete/<string:id>", methods=["DELETE"])
def manufacturer_delete(id):
    """
    通过删除生产商
    ---
    tags:
      - 生产商接口
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: 生产商ID
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关厂商的信息
      0:
        description: 查询成功
    """
    return manufacturer.manufacturer_delete(id)


@app.route(manufacturer.baseUrl + "/manufacturerUpdate/<string:id>", methods=["PUT"])
def manufacturer_update(id):
    """
    通过ID更新生产商
    ---
    tags:
      - 生产商接口
    responses:
      1001:
        description: 不可传入空
      1002:
        description: 该厂商已经存在
      0:
        description: 恭喜，修改生产厂商信息成功
    """
    return manufacturer.manufacturer_update(id)


@app.route(manufacturer.baseUrl + "/getAll", methods=["GET"])
def get_all_manufacturer():
    """
    获取所有生产商
    ---
    tags:
      - 生产商接口
    responses:
      1001:
        description: 不可传入空
      1002:
        description: 该厂商已经存在
      1003:
        description: 该厂商前缀已经存在
      0:
        description: 查询成功
    """
    return manufacturer.get_all_manufacturer()


@app.route(manufacturer.baseUrl + "/getManufacturerById/<string:id>", methods=["GET"])
def get_manufacturer_by_id(id):
    """
    通过ID获取生产商
    ---
    tags:
      - 生产商接口
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关厂商的信息
      0:
        description: 查询成功
    """
    return manufacturer.get_manufacturer_by_id(id)


@app.route(manufacturer.baseUrl + "/getManufacturerByFactoryName/<string:factory_name>", methods=["GET"])
def get_manufacturer_by_factory_name(factory_name):
    """
    通过名字获取生产商
    ---
    tags:
      - 生产商接口
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关厂商的信息
      0:
        description: 恭喜，删除检测盒信息成功
    """
    return manufacturer.get_manufacturer_by_factory_name(factory_name)


"""
下面为检测盒路由
"""


@app.route(manufacturer_detection_box.baseUrl + "/getAll", methods=["GET"])
def get_all_manufacturer_detection_box():
    """
    获取所有自检盒
    ---
    tags:
      - 自检盒接口
    responses:
      0:
        description: 查询成功
    """
    return manufacturer_detection_box.get_all_manufacturer_detection_box()


@app.route(manufacturer_detection_box.baseUrl + "/manufacturerDetectionBoxDelete/<string:id>", methods=["DELETE"])
def manufacturer_detection_box_delete(id):
    """
    通过id删除自检盒
    ---
    tags:
      - 自检盒接口
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关检测盒的信息
      0:
        description: 查询成功
    """
    return manufacturer_detection_box.manufacturer_detection_box_delete(id)


@app.route(manufacturer_detection_box.baseUrl + "/getManufacturerDetectionBoxById/<string:id>", methods=["GET"])
def get_manufacturer_detection_box_by_id(id):
    """
    通过ID获取自检盒
    ---
    tags:
      - 自检盒接口
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关检测盒的信息
      0:
        description: 查询成功
    """
    return manufacturer_detection_box.get_manufacturer_detection_box_by_id(id)


@app.route(manufacturer_detection_box.baseUrl + "/addManufacturerDetectionBox", methods=["POST"])
def add_manufacturer_detection_box():
    """
    添加自检盒
    ---
    tags:
      - 自检盒接口
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关检测盒的信息
      0:
        description: 恭喜，添加成功
    """
    return manufacturer_detection_box.add_manufacturer_detection_box()


@app.route(manufacturer_detection_box.baseUrl+"/isValidProductionSerialNumber/<string:production_serial_number>", methods=["POST"])
def is_valid_production_serial_number(production_serial_number):
    """
    判断是否有效
    ---
    tags:
      - 自检盒接口
    responses:
      1001:
        description: 不可传入空
      1004:
        description: 查不到相关检测盒的信息
      0:
        description: 检验合法
    """
    return manufacturer_detection_box.is_valid_production_serial_number(production_serial_number)


"""
下面为二维码相关路由
"""


@app.route("/api/generateQRcode/<string:my_str>", methods=["GET"])
def generate_qrcode(my_str):
    """
    生成二维码
    ---
    tags:
      - 二维码接口
    responses:
      0:
        description: 生成成功
    """
    return qr_code.generate_qrcode(my_str)


@app.route("/api/images/<image_id>.jpg", methods=["GET"])
def get_qrcode(image_id):
    """
    查看二维码
    ---
    tags:
      - 二维码接口
    responses:
      0:
        description: 查看成功
    """
    return qr_code.get_qrcode(image_id)


"""
下面为上传图片接口
"""


@app.route("/api/photo/upload", methods=['POST', "GET"])
def uploads():
    """
    上传图片
    ---
    tags:
      - 上传图片接口
    responses:
      1005:
        description: 格式错误,请上传jpg格式文件
      0:
        description: 上传成功
    """
    return upload.uploads()


"""
下面为水印接口
"""


@app.route(watermark.baseUrl+"/watermarkEmbed/<string:filePath>/<string:watermarkInfo>", methods=["POST"])
def watermark_embed(filePath, watermarkInfo):
    """
    水印嵌入
    ---
    tags:
      - 水印接口
    responses:
      0:
        description: 水印嵌入成功
    """
    return watermark.watermark_embed(filePath, watermarkInfo)


@app.route(watermark.baseUrl+"/watermarkExtract/<string:filePath>", methods=["POST"])
def watermark_extract(filePath):
    """
    水印提取
    ---
    tags:
      - 水印接口
    responses:
      0:
        description: 水印提取成功
    """
    return watermark.watermark_extract(filePath)


@app.route(user.baseUrl+"/register", methods=["POST"])
def user_register():
    """
    用户注册
    ---
    tags:
      - 用户注册接口
    responses:
      0:
        description: 注册成功
    """
    return user.register()


@app.route(user.baseUrl+"/event", methods=["POST"])
def insert_event():
    """
    事件记录
    ---
    tags:
      - 事件记录接口
    responses:
      0:
        description: 记录成功
    """
    return user.insert_event()


@app.route(covid_detect.baseUrl, methods=["POST"])
def check():
    """
    图片识别
    ---
    tags:
      - 图片识别接口
    responses:
      0:
        description: 记录成功
    """
    return covid_detect.covid_check()
