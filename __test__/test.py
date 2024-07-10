# 获取 debugger_images/find_postion_by_color 下面的所有图片
import os
import time
import cv2
import numpy as np

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

def get_images(path):
    files = os.listdir(path)
    # 返回绝对路径的图片
    files = [os.path.join(path, file) for file in files]
    return files


def find_position_by_color(image , hsv_range, draw=True):
    time.sleep(0.2)

    """
    寻找指定颜色的区域
    """
    # 读取图像
    if image is None:
        print("无法读取图像")
        return None

    # 将图像从 BGR 转换为 HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

    # 定义颜色范围
    lower_color = np.array(hsv_range[0])
    upper_color = np.array(hsv_range[1])

    # 创建颜色掩码
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 如果找到轮廓，找到最大的轮廓并绘制矩形
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        position = (x, y, x + w, y + h)
        if draw:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # 没有文件夹创建这个文件夹
            if not os.path.exists('debugger_images'):
                os.makedirs('debugger_images')
            output_path = f'./debugger_images/{time.time()}.png'
            cv2.imwrite(output_path, image)
            print(f"输出调试图像到: {output_path}")
        return position
    
    return None



def match_color():
    exclamatory_colors = ([174, 50, 0],[255, 255, 255])
    drag_bar_center_colors =([70, 110, 110],[120, 255, 255])
    drag_bar_box_colors = ([126, 0, 150],[160, 255, 255])

    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/debugger_images/find_postion_by_color-2'
    files = get_images(path)

    for file in files:
        image = cv2.imread(file)
        # position = find_position_by_color(image, exclamatory_colors)
        # if position is not None:
        #     print(f"找到了{file}的叹号位置: {position}")
        # # position = find_position_by_color(image, drag_bar_center_colors)
        # if position is not None:
        #     print(f"找到了{file}的拖动条中心位置: {position}")
        position = find_position_by_color(image, drag_bar_box_colors)
        if position is not None:
            print(f"找到了{file}的拖动条框位置: {position}")


if __name__ == '__main__':
    # match_color()

    print(rgbs2hsv("#5032F7,#4E2EE2,#6C35FB,#8731FB,#5D26DD,#6625C8,#4A30DE,#5D1AA1,#461767"))