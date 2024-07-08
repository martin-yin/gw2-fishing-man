import time
import cv2
from win32gui import SetForegroundWindow
from image_postion import FishImagePosition
from fishing import Fishing
from utils.utils import draw_position_border, get_hwnd, load_config

if __name__ == '__main__':
    hwnd = get_hwnd()
    SetForegroundWindow(hwnd)
    time.sleep(0.5)
    config = load_config("./config.yaml")
    # 获取图标位置
    fish_image_positon = FishImagePosition(config['position'])
    skill = fish_image_positon.skill_position
    exclamation = fish_image_positon.exclamation_position
    drag_hook = fish_image_positon.drag_hook_position
    drag_bar_position = fish_image_positon.drag_bar_position
    fishing = Fishing(skill, exclamation, drag_hook, drag_bar_position)
    print("绘制位置边框")
    while True:
        draw_position_border(skill)
        draw_position_border(exclamation)
        draw_position_border(drag_hook)
        draw_position_border(drag_bar_position)