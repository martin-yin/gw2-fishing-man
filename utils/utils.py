import ctypes
import win32con
from win32 import win32api, win32gui, win32print
import dxcam
import yaml

camera = None
hwnd = None

def get_hwnd():
    global hwnd
    if hwnd:
        return hwnd
    hwnd = win32gui.FindWindow(None, "激战2")
    
    return hwnd


def get_frame(region):
    global camera
    if camera is None:
        camera = dxcam.create()
        
    return camera.grab(region)


# 参数左上右下
def draw_position_border(box, color=(255, 0, 255)):
    hwnd = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hwnd)
    hPen = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(color[0], color[1], color[2]))
    win32gui.SelectObject(hwndDC, hPen)
    hbrush = win32gui.GetStockObject(win32con.NULL_BRUSH)
    prebrush = win32gui.SelectObject(hwndDC, hbrush)
    win32gui.Rectangle(hwndDC, box[0], box[1], box[2], box[3])
    win32gui.SelectObject(hwndDC, prebrush)
    win32gui.ReleaseDC(hwnd, hwndDC)
    win32gui.DeleteObject(hPen)
    return

# 计算两个坐获取到真实的坐标位置
def real_position(game_postion, target_postion):
    left = game_postion[0] + target_postion[0]
    top = game_postion[1] + target_postion[1]
    right = left + target_postion[2] - target_postion[0]
    bottom = top + target_postion[3] - target_postion[1]

    return (left, top, right, bottom)

# 计算坐标偏移
def offset_position(position, offset):
    left = position[0] + offset[0]
    top = position[1] + offset[1]
    right = position[2] + offset[2]
    bottom = position[3] + offset[3]

    return (left, top, right, bottom)


def map_virtual_key(vk_code):
    return win32api.MapVirtualKey(vk_code, 0)

# 发送键盘事件
def key_down_up(hwnd, vk_code):
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

def load_config(file_path):
    """
    读取 YAML 文件并返回配置字典

    :param file_path: YAML 文件的路径
    :return: 包含配置信息的字典
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_windows_scale():
    try:
        # 调用 Windows API 函数获取缩放比例
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()
 
        # 计算缩放比例
        return scaling_factor / 96.0
 
    except Exception as e:
        exit("获取 windows dpi 失败")
        return None