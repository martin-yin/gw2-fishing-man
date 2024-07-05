import time
import cv2
from gw2_window import GW2Window
from utils.match_image import extract_blue_area, extract_green_area
from utils.utils import Camera, key_down, key_up

class Fishing:
    def __init__(self,  hwnd, carmera: Camera, drag_bar_position):
        self.hwnd = hwnd
        self.carmera = carmera
        self.drag_bar_position = drag_bar_position
        
    def drag_action(self):
        bar_image = self.carmera.get_frame(self.drag_bar_position)
        bar_center_box, bar_center_position = extract_green_area(bar_image, False)
        bar_box, bar_position = extract_blue_area(bar_image, False)
        if bar_center_box is None or bar_box is None:
            return
        
        bar_center_middle = (bar_center_box[0] + bar_center_box[2]) / 2
        bar_middle = (bar_box[0] + bar_box[2]) / 2

        dead_zone = 2

        if abs(bar_center_middle - bar_middle) <= dead_zone:
            # 在死区范围内，不进行任何调整
            key_up(self.hwnd, 48 + 2)
            key_up(self.hwnd, 48 + 3)
            return

        if bar_center_middle < bar_middle - dead_zone:
            key_up(self.hwnd, 48 + 3)
            key_down(self.hwnd, 48 + 2)
         
        elif bar_center_middle > bar_middle + dead_zone:
            key_up(self.hwnd, 48 + 2)
            key_down(self.hwnd, 48 + 3)
         
            