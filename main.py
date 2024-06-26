import time
import cv2
import numpy as np
from fishing import Fishing
from gw2_window import GW2Window
from PIL import Image

from utils.show_target import Show_target

# def extract_blue_area(image):
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     lower_blue = np.array([100, 50, 50])
#     upper_blue = np.array([130, 255, 255])

#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     cv2.imwrite(f'{time.time()}.png', image)

if __name__ == '__main__':
    gw2 = GW2Window()
    fish = Fishing(gw2)
    fish.init_position()
    fish.reset_fish_state()
    while True:
       fish.get_fish_state()
