import math
import random
import numpy as np
from scipy import misc, ndimage
import os
import matplotlib.pyplot as plt
import cv2

from cnstd import CnStd
from cnocr import CnOcr

# 存放线条检测结果
list = []
# 红色区间1
lower_red = np.array([156, 43, 46])
upper_red = np.array([180, 255, 255])

# 红色区间2
lower_red0 = np.array([0, 43, 46])
upper_red0 = np.array([10, 255, 255])
# 紫色区间
lower_purple = np.array([125, 43, 46])
upper_purple = np.array([155, 255, 255])


def line_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # apertureSize做Canny时梯度窗口的大小
    edges = cv2.Canny(gray, 30, 150, apertureSize=3)
    # 返回的是r和theta
    lines = cv2.HoughLines(edges, 1, np.pi/180, 9)
    if lines is None:
        return 0
    else:
        return 1


def detect(filepath):
    # 1.读图片，倾斜校正
    img = cv2.imread(filename=filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 霍夫变换
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
    if x1 == x2 or y1 == y2:
        return
    t = float(y2 - y1) / (x2 - x1)
    rotate_angle = math.degrees(math.atan(t))
    if rotate_angle > 45:
        rotate_angle = -90 + rotate_angle
    elif rotate_angle < -45:
        rotate_angle = 90 + rotate_angle
    rotate_img = ndimage.rotate(img, rotate_angle)

    # 2.文本区域检测，文字识别C与T
    std = CnStd()
    cn_ocr = CnOcr()

    box_infos = std.detect(rotate_img)
    for box_info in box_infos['detected_texts']:
        a = box_info['box'][2][0] - box_info['box'][0][0]
        b = box_info['box'][2][1] - box_info['box'][0][1]
        if (int(a) == 0 or int(b) == 0):
            continue
        if (int(a) / int(b) < 1.1):
            cropped_img = box_info['cropped_img']
            ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
            if (ocr_res['score'] > 0.45):
                if (ocr_res['text'] == 'C' or ocr_res['text'] == 'T'):
                    # i = i + 1
                    # print(box_info['box'])
                    # print('result: %s' % str(ocr_res))
                    aa = box_info['box'][0][0]
                    bb = box_info['box'][0][1]
                    cc = box_info['box'][2][0]
                    dd = box_info['box'][2][1]

                    pt1 = (int(aa), int(bb))
                    pt2 = (int(cc), int(dd))

                    # 3.由C与T的位置定位对应红线位置

                    x1 = round(aa - round((cc - aa) * 1.5))
                    x0 = round(x1 - (cc - aa) * 2)
                    y0 = round(bb - round((dd - bb) / 2))
                    y1 = round(dd + round((dd - bb) / 2))
                    crop_img = rotate_img[y0:y1, x0:x1]

                    # 4.取出红线位置，提取红色区域

                    frame = crop_img
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask0 = cv2.inRange(hsv, lower_red0, upper_red0)
                    mask1 = cv2.inRange(hsv, lower_red, upper_red)
                    mask2 = cv2.inRange(hsv, lower_purple, upper_purple)
                    mask = mask0 + mask1 + mask2
                    res = cv2.bitwise_and(frame, frame, mask=mask)

                    # 5.检测线条是否存在并保存结果
                    line = line_detection(res)
                    list.append(line)

        # 6.由线条存在情况判断最终结果
        if (list is None or len(list) < 2):
            return '识别失败'
        elif (list[0] == 1 and list[1] == 1):
            return '阳性'
        elif (list[0] == 1 and list[1] == 0):
            return '阴性'
        else:
            return '无结果'
