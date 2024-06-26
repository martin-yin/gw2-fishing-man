from win32 import win32api, win32gui, win32print
from win32.lib import win32con
import ctypes
import win32ui
import dxcam
from PIL import Image
import cv2
import numpy as np


class GW2Window:
    def __init__(self, game_name = "激战2"):
        self.hwnd = win32gui.FindWindow(None, game_name)
        user32 = ctypes.windll.user32
        user32.GetDpiForSystem()
        self.get_size()
        self.get_window_position()
        self.get_center_position()
        self.camera = dxcam.create()

    def get_size(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.size = (right - left, bottom - top)


    def get_window_position(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.position = (left, top, right, bottom)

    def get_center_position(self):
        game_size = self.size
        game_position = self.position
        centerx = (game_size[0] / 2)  +  game_position[0]
        centery = (game_size[1]  /2 ) + game_position[1]
        self.center_position = (int(centerx), int(centery))

    def acitvation_window(self):
        win32gui.SetForegroundWindow(self.hwnd)

    def get_windows_dpi_scale(self):
        user32 = ctypes.windll.user32
        user32.GetDpiForSystem()
        user32.GetDpiForWindow.restype = ctypes.c_uint
        dpi = user32.GetDpiForWindow(user32.GetDesktopWindow())
        self.dpi_scale =  dpi / 96 

    # 键盘 key 映射
    def map_virtual_key(vk_code):
        return win32api.MapVirtualKey(vk_code, 0)

    # 发送键盘事件
    def post_key_event(self, vk_code):
        scan_code = self.map_virtual_key(vk_code)
        key_up_lParam = (win32con.KEYEVENTF_SCANCODE << 16) | scan_code
        key_down_lParam = ( win32con.KEYEVENTF_SCANCODE | win32con.KEYEVENTF_KEYUP << 16) | scan_code
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code, key_up_lParam)
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, key_down_lParam)

    def window_screenshot(self, region=None):
        # 游戏的窗口截图
        if region is None:
            region = self.position
            
        return self.camera.grab(region=region)
    
    