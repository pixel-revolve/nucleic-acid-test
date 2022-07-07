import hashlib
from config.setting import MD5_SALT


def get_md5(serial_number):
    """MD5加密处理"""
    str = serial_number + MD5_SALT  # 将前缀和随机字符串和加入盐值然后md5加密
    md5 = hashlib.md5()  # 创建md5对象
    md5.update(str.encode("utf-8"))  # Python3中需要先转换为 bytes 类型，才能加密
    return md5.hexdigest()  # 返回密文
