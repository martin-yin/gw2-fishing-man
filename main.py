import time
from win32gui import SetForegroundWindow
from image_postion import FishImagePosition
from fishing import Fishing
from utils.utils import get_hwnd, load_config

if __name__ == '__main__':
    hwnd = get_hwnd()
    SetForegroundWindow(hwnd)
    time.sleep(0.5)
    config = load_config("./config-4k.yaml")
    # 获取图标位置
    fish_image_positon = FishImagePosition(config['position'])
    skill = fish_image_positon.skill_position
    exclamation = fish_image_positon.exclamation_position
    drag_hook = fish_image_positon.drag_hook_position
    drag_bar_position = fish_image_positon.drag_bar_position
    fishing = Fishing(skill, exclamation, drag_hook, drag_bar_position)
    print("开始钓鱼")
    fishing.reset()
    while True:
        fishing.get_state()