from common import check
from flask import jsonify
from requests import request

baseUrl = '/api/check'

def detetct():
  """结果检测"""
  file_path = request.json.get('filePath','').strip()
  data = check.detect(file_path)
  return jsonify({"code": 0, "data": data, "msg": "查询成功"})