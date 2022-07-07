import random
import uuid

from common.mysql_operate import db
from flask import jsonify, request
from common.md5_operate import get_md5
from api.qr_code import generate_qrcode, get_current_milli_time

baseUrl = "/manufacturerDetectionBox"


def get_all_manufacturer_detection_box():
    """获取所有检测盒信息"""
    sql = "SELECT * FROM manufacturer_detection_box"
    data = db.select_db(sql)
    print("获取所有检测盒信息 == >> {}".format(data))
    return jsonify({"code": 0, "data": data, "msg": "查询成功"})


def add_manufacturer_detection_box():
    factory_id = request.json.get("factory_id", "").strip()  # 检测盒Id
    if factory_id:  # 注意if条件中 "" 也是空, 按False处理
        """首先获取对应厂商信息"""
        sql1 = "SELECT * FROM manufacturer WHERE id = '{}'".format(factory_id)
        data = db.select_db(sql1)
        if data:
            manufacturer_detection_box = data[0]
            factory_prefix = manufacturer_detection_box['factory_prefix']
            random_str = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))  # 获得随机数
            production_serial_number = factory_prefix + random_str + str(get_current_milli_time())  # 为保证生产序列号唯一再加上时间戳
            # 根据生产厂商序列号生成二维码
            generate_qrcode(production_serial_number)
            md5_result = get_md5(production_serial_number)
            # 根据md5结果生成二维码
            generate_qrcode(md5_result)

            """将信息存入数据库"""
            id = uuid.uuid1()
            sql2 = "INSERT INTO manufacturer_detection_box(id,factory_id,production_serial_number,md5_result) " \
                   "VALUES('{}', '{}', '{}','{}')".format(id, factory_id, production_serial_number, md5_result)
            db.execute_db(sql2)
            print("新增检测盒信息SQL ==>> {}".format(sql2))
            return jsonify({"code": 0, "msg": "恭喜，添加成功！"})

        return jsonify({"code": "1004", "msg": "查不到相关检测盒的信息"})

    return jsonify({"code": 1001, "msg": "不可传入空"})


def get_manufacturer_detection_box_by_id(id):
    if id:
        """获取某个检测盒信息"""
        sql = "SELECT * FROM manufacturer_detection_box WHERE id = '{}'".format(id)
        data = db.select_db(sql)
        print("获取 {} 检测盒信息 == >> {}".format(id, data))
        if data:
            return jsonify({"code": 0, "data": data, "msg": "查询成功"})
        return jsonify({"code": "1004", "msg": "查不到相关检测盒的信息"})
    return jsonify({"code": 1001, "msg": "不可传入空"})


def manufacturer_detection_box_delete(id):
    if id:
        sql1 = "SELECT * FROM manufacturer_detection_box WHERE id = '{}'".format(id)
        data = db.select_db(sql1)
        if data:
            sql2 = "DELETE FROM manufacturer_detection_box WHERE id = '{}'".format(id)
            db.execute_db(sql2)
            print("删除检测盒信息SQL ==>> {}".format(sql2))
            return jsonify({"code": 0, "msg": "恭喜，删除检测盒信息成功！"})
        return jsonify({"code": "1004", "msg": "查不到相关检测盒的信息"})
    return jsonify({"code": 1001, "msg": "不可传入空"})


def is_valid_production_serial_number(production_serial_number):
    if production_serial_number:
        md5_result = get_md5(production_serial_number)
        # sql1 = "SELECT * FROM manufacturer_detection_box WHERE production_serial_number = '{}'".format(production_serial_number)
        # data = db.select_db(sql1)
        # if data:
        #     get_md5_result = data[0]['md5_result']
        #     if get_md5_result == md5_result:
        #         return jsonify({"code": 0, "msg": "检验合法"})
        sql1 = "SELECT * FROM manufacturer_detection_box WHERE md5_result = '{}'".format(md5_result)
        data = db.select_db(sql1)
        if data:
            return jsonify({"code": 0, "msg": "检验合法"})

        return jsonify({"code": "1004", "msg": "查不到相关检测盒的信息"})
    return jsonify({"code": 1001, "msg": "不可传入空"})
