
import cv2
from PIL import Image
import numpy as np
import time

def non_max_suppression_fast(boxes, overlapThresh):
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []

    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")


def match_image(image, template, draw=False):
    """ 
        image: 需要被匹配的图片
        template: 模板图片
    """
    if template is None:
        return []
    
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    rectangles = []
    for pt in zip(*loc[::-1]):
        rect = [int(pt[0]), int(pt[1]), int(pt[0] + image.shape[1]), int(pt[1] + image.shape[0])]
        rectangles.append(rect)
        rectangles.append(rect)  

    rectangles = np.array(rectangles)
    pick = non_max_suppression_fast(rectangles, 0.8)

    for (x1, y1, x2, y2) in pick:
        if draw:
            cv2.rectangle(template, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if draw:
        timestr = time.strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f'./match_image/{timestr}.png', template)

    return pick


def macth_red_exclamatory(image, debug=False):
    if image is None:
        return []
    is_find = False
    lower_purple = np.array([125, 70, 70]) 
    upper_purple = np.array([155, 255, 255]) 

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    timestr = time.strftime("%Y%m%d_%H%M%S")

    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(contour)
        if 0.5 < aspect_ratio < 1.3 and 350 < area < 1000:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            is_find = True
            break

    if is_find and debug:
        cv2.imwrite(f'./find_purple/debug-{timestr}.png', image)
    
    return is_find


def match_bar_position(template_image, target_image, draw=False, borderColor=(0, 255, 0), borderThickness=2):
    if template_image is None:
        return (None, None)
    
    if target_image is None:
        return (None, None)
    
    match_result = cv2.matchTemplate(target_image, template_image, cv2.TM_CCOEFF_NORMED)
    min_val_orange, max_val_orange, min_loc_orange, max_loc_orange = cv2.minMaxLoc(match_result)
    center = (max_loc_orange[0] + template_image.shape[1] / 2, max_loc_orange[1] + template_image.shape[0] / 2)
    postion = (max_loc_orange[0], max_loc_orange[1], max_loc_orange[0] + template_image.shape[1], max_loc_orange[1] + template_image.shape[0])

    if draw:
        cv2.rectangle(target_image, (max_loc_orange[0], max_loc_orange[1]), 
                      (max_loc_orange[0] + template_image.shape[1], max_loc_orange[1] + template_image.shape[0]), borderColor, borderThickness)
        target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f'./match_bar_position/debug-{time.strftime("%Y%m%d_%H%M%S")}.png', target_image)

    return postion, center


def extract_green_area(image, draw=False):
    if image is None:
        return (None, None)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(sorted_contours) == 0:
        return None, None
    
    best_contour = sorted_contours[0]

    x, y, w, h = cv2.boundingRect(best_contour)
    
    if draw:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(f'./extract_greeen_area/debug-{time.strftime("%Y%m%d_%H%M%S")}.png', image)

    position = (x, y, x + w, y + h)
    center = (x + w / 2, y + h / 2)
    
    return position, center

def extract_blue_area(image, draw=False):
    if image is None:
        return (None, None)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array( [80, 100, 100])
    upper_blue = np.array([110, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(sorted_contours) == 0:
        return None, None
    
    best_contour = sorted_contours[0]
    x, y, w, h = cv2.boundingRect(best_contour)
    
    if draw:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(f'./extract_blue_area/debug-{time.strftime("%Y%m%d_%H%M%S")}.png', image)

    position = (x, y, x + w, y + h)
    center = (x + w / 2, y + h / 2)
    
    return position, center

# 判断钓鱼鱼钩图是否存在

def match_hook(image, template_image, draw=False):
    """ 
        image: 需要被匹配的图片
        template: 模板图片
    """
    if template_image is None:
        return (None, None)
    
    match_result = cv2.matchTemplate(image, cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
    min_val_orange, max_val_orange, min_loc_orange, max_loc_orange = cv2.minMaxLoc(match_result)

    if max_val_orange > 0.7:
        center = (max_loc_orange[0] + template_image.shape[1] / 2, max_loc_orange[1] + template_image.shape[0] / 2)
        postion = (max_loc_orange[0], max_loc_orange[1], max_loc_orange[0] + template_image.shape[1], max_loc_orange[1] + template_image.shape[0])
        # if draw:
        #     cv2.rectangle(target_image, (max_loc_orange[0], max_loc_orange[1]), 
        #                   (max_loc_orange[0] + template_image.shape[1], max_loc_orange[1] + template_image.shape[0]), (0, 255, 0), 2)
        #     target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
        #     cv2.imwrite(f'./match_hook/debug-{time.strftime("%Y%m%d_%H%M%S")}.png', target_image)
        return postion, center
    
    else:
        return None, None



def get_score_width(image):
    # https://www.jiniannet.com/Page/allcolor 这里取得图片的相邻像素的颜色
    # 
    # 转化为HSV图像
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imwrite('hsvw.png', hsv_image)

    # 定义橙色的HSV阈值范围
    lower_orange = np.array([15, 162, 255])
    upper_orange = np.array([30, 162, 255])

    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        return w
    return None


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
