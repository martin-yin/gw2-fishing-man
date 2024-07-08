
import cv2
from PIL import Image
import numpy as np
import time

from utils.utils import get_windows_scale

# def get_score_width(image):
#     # https://www.jiniannet.com/Page/allcolor 这里取得图片的相邻像素的颜色
#     # 
#     # 转化为HSV图像
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     cv2.imwrite('hsvw.png', hsv_image)

#     # 定义橙色的HSV阈值范围
#     lower_orange = np.array([15, 162, 255])
#     upper_orange = np.array([30, 162, 255])

#     mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
#     # 查找轮廓
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     if len(contours) > 0:
#         largest_contour = max(contours, key=cv2.contourArea)
#         x, y, w, h = cv2.boundingRect(largest_contour)
        
#         return w
#     return None


# 临近颜色转 hsv
# import cv2
# import numpy as np

# rgb = '#FFAC5D,#FFB85D,#FFBC5D,#FFD95D'

# rgb = rgb.split(',')

# # 转换为BGR格式，并将16进制转换为10进制
# bgr = [[int(r[5:7], 16), int(r[3:5], 16), int(r[1:3], 16)] for r in rgb]

# # 转换为HSV格式
# hsv = [list(cv2.cvtColor(np.uint8([[b]]), cv2.COLOR_BGR2HSV)[0][0]) for b in bgr]

# hsv = np.array(hsv)
# print('H:', min(hsv[:, 0]), max(hsv[:, 0]))
# print('S:', min(hsv[:, 1]), max(hsv[:, 1]))
# print('V:', min(hsv[:, 2]), max(hsv[:, 2]))


def rgbs2hsv(rgbs):
    """
        将颜色字符串转换为hsv格式
    """
    rgb = rgbs.split(',')
    # 转换为BGR格式，并将16进制转换为10进制
    bgr = [[int(r[5:7], 16), int(r[3:5], 16), int(r[1:3], 16)] for r in rgb]
    # 转换为HSV格式
    hsv = [list(cv2.cvtColor(np.uint8([[b]]), cv2.COLOR_BGR2HSV)[0][0]) for b in bgr]
    hsv = np.array(hsv)

    lower_color = np.array([min(hsv[:, 0]), min(hsv[:, 1]), min(hsv[:, 2])])
    upper_color = np.array([max(hsv[:, 0]), max(hsv[:, 1]), max(hsv[:, 2])])
    return (lower_color, upper_color)

def match_image(image, template, draw=True): 
    """ 
        image: 截图图片
        template: images下的图片
    """
    if image is None:
        return None
    
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dpi = get_windows_scale()
    # 缩放后的模板图片
    scaled_template = cv2.resize(template, (0, 0), fx=dpi, fy=dpi)
    match_result = cv2.matchTemplate(image_gray, scaled_template,  cv2.TM_CCOEFF_NORMED)
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(match_result)
    
    if max_val > 0.9:
        (x, y) = max_loc
        w, h = template.shape[:2]
        end_x = x + w
        end_y = y + h
        position = (x, y, end_x, end_y)
        if draw:
            # cv2.rectangle(image, (x, y), (end_x, end_y), (0, 255, 0), 2)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f'./debugger_images/match_image/{time.strftime("%Y%m%d_%H%M%S")}.png', image)
        return position
    
    return None


def find_postion_by_color(image, colors, draw=False):
    """
    寻找指定颜色的区域
    """
    if image is None:
        return None

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_color = np.array(colors[0])
    upper_color = np.array(colors[1])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        position = (x, y, x + w, y + h)
        if draw:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imwrite(f'./debugger_images/find_postion_by_color/{time.strftime("%Y%m%d_%H%M%S")}.png', image)
        return position
    
    return None