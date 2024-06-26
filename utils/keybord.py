import win32con
from win32 import win32api, win32gui
import time

def map_virtual_key(vk_code):
    return win32api.MapVirtualKey(vk_code, 0)

# 发送键盘事件
def post_key_event(hwnd, vk_code):
    scan_code = map_virtual_key(vk_code)

    lParam_KeyDown = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (0 << 31)
    lParam_KeyUp = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (1 << 30) | (1 << 31)
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lParam_KeyDown)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code,lParam_KeyUp)

def key_down(hwnd, vk_code):
    scan_code = map_virtual_key(vk_code)
    lParam_KeyDown = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (0 << 31)
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lParam_KeyDown)

def key_up(hwnd, vk_code):
    scan_code = map_virtual_key(vk_code)
    lParam_KeyUp = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (1 << 30) | (1 << 31)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code,lParam_KeyUp)