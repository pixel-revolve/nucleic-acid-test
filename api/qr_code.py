import qrcode
import time
import os

from flask import Response


def get_current_milli_time():
    return int(round(time.time() * 1000))


basedir = os.path.abspath('.')
qrcode_dir = basedir+"\\static\\images\\qrcode\\"
qr = qrcode.QRCode()


def generate_qrcode(my_str):
    """根据字符串生成二维码"""
    qr.add_data(my_str)
    img = qr.make_image(fill_color='black', back_color='white')
    image_name = qrcode_dir+str(get_current_milli_time()) + '.jpg'
    # 将二维码保存为图片
    with open(image_name, 'wb') as f:
        img.save(f)
    return image_name


def get_qrcode(image_id):
    # 图片上传保存的路径
    with open(qrcode_dir+"{}.jpg".format(image_id), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp
