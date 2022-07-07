from flask import Flask, jsonify, request
import api.manufacturer as manufacturer
import api.manufacturer_detection_box as manufacturer_detection_box
import api.qr_code as qr_code
import api.upload as upload
import api.watermark as watermark

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示

"""
下面为生产厂商相关路由注册
"""


@app.route(manufacturer.baseUrl + "/addManufacturer", methods=["POST"])
def add_manufacturer():
    return manufacturer.add_manufacturer()


@app.route(manufacturer.baseUrl + "/manufacturerDelete/<string:id>", methods=["DELETE"])
def manufacturer_delete(id):
    return manufacturer.manufacturer_delete(id)


@app.route(manufacturer.baseUrl + "/manufacturerUpdate/<string:id>", methods=["PUT"])
def manufacturer_update(id):
    return manufacturer.manufacturer_update(id)


@app.route(manufacturer.baseUrl + "/getAll", methods=["GET"])
def get_all_manufacturer():
    return manufacturer.get_all_manufacturer()


@app.route(manufacturer.baseUrl + "/getManufacturerById/<string:id>", methods=["GET"])
def get_manufacturer_by_id(id):
    return manufacturer.get_manufacturer_by_id(id)


@app.route(manufacturer.baseUrl + "/getManufacturerByFactoryName/<string:factory_name>", methods=["GET"])
def get_manufacturer_by_factory_name(factory_name):
    return manufacturer.get_manufacturer_by_factory_name(factory_name)


"""
下面为检测盒路由
"""


@app.route(manufacturer_detection_box.baseUrl + "/getAll", methods=["GET"])
def get_all_manufacturer_detection_box():
    return manufacturer_detection_box.get_all_manufacturer_detection_box()


@app.route(manufacturer_detection_box.baseUrl + "/manufacturerDetectionBoxDelete/<string:id>", methods=["DELETE"])
def manufacturer_detection_box_delete(id):
    return manufacturer_detection_box.manufacturer_detection_box_delete(id)


@app.route(manufacturer_detection_box.baseUrl + "/getManufacturerDetectionBoxById/<string:id>", methods=["GET"])
def get_manufacturer_detection_box_by_id(id):
    return manufacturer_detection_box.get_manufacturer_detection_box_by_id(id)


@app.route(manufacturer_detection_box.baseUrl + "/addManufacturerDetectionBox", methods=["POST"])
def add_manufacturer_detection_box():
    return manufacturer_detection_box.add_manufacturer_detection_box()


@app.route(manufacturer_detection_box.baseUrl+"/isValidProductionSerialNumber/<string:production_serial_number>", methods=["POST"])
def is_valid_production_serial_number(production_serial_number):
    return manufacturer_detection_box.is_valid_production_serial_number(production_serial_number)


"""
下面为二维码相关路由
"""


@app.route("/generateQRcode/<string:my_str>", methods=["POST"])
def generate_qrcode(my_str):
    return qr_code.generate_qrcode(my_str)


@app.route("/images/<image_id>.jpg", methods=["GET"])
def get_qrcode(image_id):
    """查看二维码"""
    return qr_code.get_qrcode(image_id)


"""
下面为上传图片接口
"""


@app.route("/photo/upload", methods=['POST', "GET"])
def uploads():
    return upload.uploads()


"""
下面为水印接口
"""


@app.route(watermark.baseUrl+"/watermarkEmbed/<string:filePath>/<string:watermarkInfo>", methods=["POST"])
def watermark_embed(filePath, watermarkInfo):
    return watermark.watermark_embed(filePath, watermarkInfo)


@app.route(watermark.baseUrl+"/watermarkExtract/<string:filePath>", methods=["POST"])
def watermark_extract(filePath):
    return watermark.watermark_extract(filePath)
