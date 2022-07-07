import os

from flask import Flask, Response, request, render_template
from werkzeug.utils import secure_filename

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']

basedir = os.path.abspath('.')
images_dir = basedir+"\\static\\images\\"


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        file = request.files['file']
        if file and allowed_file(file.filename):
            print(file.filename)
            # secure_filename方法会去掉文件名中的中文
            file_name = secure_filename(file.filename)
            # 保存图片
            file.save(os.path.join(images_dir, file_name))
            return "success"
        else:
            return "格式错误，请上传jpg格式文件"
    return render_template("index.html")
