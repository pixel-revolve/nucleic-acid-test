import os
from uuid import uuid1
from flask import Flask, jsonify, request, render_template

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
IMAGES_FILE = 'static/images/'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


def generateName(filename):
    return str(uuid1()) + '.' + filename.rsplit('.', 1)[1]


def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        file = request.files['file']
        if file and allowed_file(file.filename):
            # 使用自定义文件名保存图片（这里采用UUID）
            filename = generateName(file.filename)
            path = os.path.join(IMAGES_FILE, filename)
            print(path)
            # 保存图片
            file.save(path)
            return jsonify({"code": 0, "data": path, "msg": "上传成功"})
        else:
            return jsonify({"code": 1005, "msg": "格式错误,请上传jpg格式文件"})
    return render_template("index.html")
