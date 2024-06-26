import win32gui
import win32api
import win32gui
import win32con


# 参数左上右下
def Show_target(box):
    hwnd = win32gui.GetDesktopWindow()
    hPen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 255))  # 定义框颜色
    hwndDC = win32gui.GetDC(hwnd)  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    win32gui.SelectObject(hwndDC, hPen)
    hbrush = win32gui.GetStockObject(win32con.NULL_BRUSH)  # 定义透明画刷，这个很重要！！
    prebrush = win32gui.SelectObject(hwndDC, hbrush)
    win32gui.Rectangle(hwndDC, box[0], box[1], box[2], box[3])  # 左上到右下的坐标
    win32gui.SaveDC(hwndDC)
    win32gui.SelectObject(hwndDC, prebrush)
    win32gui.ReleaseDC(hwnd, hwndDC)
    return

# 计算两个坐获取到真实的坐标位置
def real_position(game_postion, target_postion):
    left = game_postion[0] + target_postion[0]
    top = game_postion[1] + target_postion[1]
    right = left + target_postion[2] - target_postion[0]
    bottom = top + target_postion[3] - target_postion[1]
    
    return (left, top, right, bottom)