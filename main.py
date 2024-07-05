import time
from win32gui import FindWindow, SetForegroundWindow
from environment.image_postion import FishImagePosition
from environment.state import FishingState
from fishing import Fishing
from utils.utils import Camera, load_config

if __name__ == '__main__':
    hwnd = FindWindow(None, "激战2")
    carmera = Camera()
    SetForegroundWindow(hwnd)
    time.sleep(1)
    config = load_config("./config.yaml")
    # 获取图标位置
    fish_image_positon = FishImagePosition(hwnd, carmera, config['position'])

    skill = fish_image_positon.skill_position
    exclamation = fish_image_positon.exclamation_position
    drag_hook = fish_image_positon.drag_hook_position
    drag_bar_position = fish_image_positon.drag_bar_position

    fish_state = FishingState(hwnd, carmera,skill, exclamation, drag_hook)

    fishing = Fishing(hwnd, carmera, drag_bar_position)

    print("开始钓鱼")
    while True:
        state = fish_state.get_state()  
        
        if state == 1:
            print("等待鱼儿上钩")
            time.sleep(0.5)
            
        if state == 2:
            fishing.drag_action()
        