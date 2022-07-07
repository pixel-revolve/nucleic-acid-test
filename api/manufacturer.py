from common.mysql_operate import db
from flask import jsonify, request
import uuid

baseUrl = "/manufacturer"


def get_all_manufacturer():
    """获取所有生产厂商信息"""
    sql = "SELECT * FROM manufacturer"
    data = db.select_db(sql)
    print("获取所有生产厂商信息 == >> {}".format(data))
    return jsonify({"code": 0, "data": data, "msg": "查询成功"})


def add_manufacturer():
    factory_name = request.json.get("factory_name", "").strip()  # 生产厂商名
    factory_prefix = request.json.get("factory_prefix", "").strip()  # 厂商前缀

    if factory_name and factory_prefix:  # 注意if条件中 "" 也是空, 按False处理
        sql1 = "SELECT * FROM manufacturer WHERE factory_name = '{}'".format(factory_name)
        data = db.select_db(sql1)
        if data:
            return jsonify({"code": 1002, "msg": "该厂商已经存在"})
        sql2 = "SELECT * FROM manufacturer WHERE factory_prefix = '{}'".format(factory_prefix)
        data = db.select_db(sql2)
        if data:
            return jsonify({"code": 1003, "msg": "该厂商前缀已经存在"})
        id = uuid.uuid1()  # 厂商的唯一id
        sql3 = "INSERT INTO manufacturer(id,factory_name,factory_prefix) " \
               "VALUES('{}', '{}', '{}')".format(id, factory_name, factory_prefix)
        db.execute_db(sql3)
        print("新增生产厂商信息SQL ==>> {}".format(sql2))
        return jsonify({"code": 0, "msg": "恭喜，添加成功！"})

    return jsonify({"code": 1001, "msg": "不可传入空"})


def get_manufacturer_by_factory_name(factory_name):
    if factory_name:
        """获取某个生产厂商信息"""
        sql = "SELECT * FROM manufacturer WHERE factory_name = '{}'".format(factory_name)
        data = db.select_db(sql)
        print("获取 {} 生产厂商信息 == >> {}".format(factory_name, data))
        if data:
            return jsonify({"code": 0, "data": data, "msg": "查询成功"})
        return jsonify({"code": "1004", "msg": "查不到相关厂商的信息"})
    return jsonify({"code": 1001, "msg": "不可传入空"})


def get_manufacturer_by_id(id):
    if id:
        """获取某个生产厂商信息"""
        sql = "SELECT * FROM manufacturer WHERE id = '{}'".format(id)
        data = db.select_db(sql)
        print("获取 {} 生产厂商信息 == >> {}".format(id, data))
        if data:
            return jsonify({"code": 0, "data": data, "msg": "查询成功"})
        return jsonify({"code": "1004", "msg": "查不到相关厂商的信息"})
    return jsonify({"code": 1001, "msg": "不可传入空"})


def manufacturer_update(id):  # id为准备修改的生产厂商ID
    """修改生产厂商信息"""
    factory_name = request.json.get("factory_name", "").strip()  # 生产厂商名
    factory_prefix = request.json.get("factory_prefix", "").strip()  # 厂商前缀

    if id and factory_name and factory_prefix:  # 注意if条件中空串 "" 也是空, 按False处理
        """首先查看修改后的名字是否已经在数据库中"""
        sql = "SELECT * FROM manufacturer WHERE factory_name = '{}'".format(factory_name)
        data = db.select_db(sql)
        if data:
            return jsonify({"code": 1002, "msg": "该厂商已经存在"})
        sql2 = "UPDATE manufacturer SET factory_name = '{}', factory_prefix = '{}' " \
               "WHERE id = '{}'".format(factory_name, factory_prefix, id)
        db.execute_db(sql2)
        print("修改生产厂商信息SQL ==>> {}".format(sql2))
        return jsonify({"code": 0, "msg": "恭喜，修改生产厂商信息成功！"})

    return jsonify({"code": 1001, "msg": "不可传入空"})


def manufacturer_delete(id):
    if id:
        sql1 = "SELECT * FROM manufacturer WHERE id = '{}'".format(id)
        data = db.select_db(sql1)
        if data:
            sql2 = "DELETE FROM manufacturer WHERE id = '{}'".format(id)
            db.execute_db(sql2)
            print("删除生产厂商信息SQL ==>> {}".format(sql2))
            return jsonify({"code": 0, "msg": "恭喜，删除生产厂商信息成功！"})
        return jsonify({"code": "1004", "msg": "查不到相关厂商的信息"})
    return jsonify({"code": 1001, "msg": "不可传入空"})
