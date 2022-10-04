import json
import re
from sqlite3 import dbapi2
from flask import jsonify, request
from pymysql import NULL
from common.mysql_operate import db

baseUrl = "/api/user"

def register():
  """用户注册"""
  open_id = request.json.get("open_id","").strip()
  sql_detect = "select * from sys_user where open_id = '{}'".format(open_id)
  get_user = db.select_db(sql_detect)
  if get_user:
    return jsonify({"code": 1, "msg": "用户已存在"})
  name = request.json.get('name','').strip()
  print(name)
  phone = request.json.get('phone','').strip()
  print(phone)
  id_card = request.json.get('id_card','').strip()
  print(id_card)
  sql_insert = "insert into sys_user (open_id,name,phone,id_card) values('{}','{}','{}','{}')".format(open_id,name,phone,id_card)
  data = db.execute_db(sql_insert)
  return jsonify({"code": 0, "data": data,"msg": "注册成功"})

def insert_event():
  user_id = request.json.get("user_id")
  test_result = request.json.get("test_result")
  sql = "insert into sys_event_detect (user_id, test_result) values ('{}','{}')".format(user_id, test_result)
  data = db.execute_db(sql)
  return jsonify({"code": 0, "data": data,"msg": "事件添加成功"})