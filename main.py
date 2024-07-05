import time
import cv2
from win32gui import FindWindow, GetWindowRect, SetForegroundWindow, GetDesktopWindow
import numpy as np
import ctypes
from fishing import Fishing
from gw2_window import GW2Window
from PIL import Image
import win32gui
import win32api
import win32gui
import win32con

from utils.show_target import position_border_draw

# from utils.show_target import Show_target
if __name__ == '__main__':
    gw2 = GW2Window()
    fish = Fishing(gw2)
    fish.init_position()
    fish.reset_fish_state()
    hwnd = FindWindow(None, "激战2")


    time.sleep(1)
    while True:
        fish.fish_action()
        # box = (50, 50, 200, 200) 
        # position_border_draw(hwnd, box)
        
        