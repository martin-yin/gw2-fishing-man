import time
import cv2
from utils.match_image import extract_blue_area, extract_green_area
from utils.utils import get_frame, get_hwnd, key_down, key_up

class Fishing:
    def __init__(self, drag_bar_position):
        self.drag_bar_position = drag_bar_position
        
    def drag_action(self):
        hwnd = get_hwnd()
        bar_image = get_frame(self.drag_bar_position)
        bar_center_box, _ = extract_green_area(bar_image, False)
        bar_box, _ = extract_blue_area(bar_image, False)
        if bar_center_box is None or bar_box is None:
            return
        
        bar_center_middle = (bar_center_box[0] + bar_center_box[2]) / 2
        bar_middle = (bar_box[0] + bar_box[2]) / 2

        dead_zone = 2

        if abs(bar_center_middle - bar_middle) <= dead_zone:
            # 在死区范围内，不进行任何调整
            key_up(hwnd, 48 + 2)
            key_up(hwnd, 48 + 3)
            return

        if bar_center_middle < bar_middle - dead_zone:
            key_up(hwnd, 48 + 3)
            key_down(hwnd, 48 + 2)
         
        elif bar_center_middle > bar_middle + dead_zone:
            key_up(hwnd, 48 + 2)
            key_down(hwnd, 48 + 3)
         
            