import time
from win32gui import FindWindow, SetForegroundWindow
from environment.image_postion import FishImagePosition
from environment.state import FishingState
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
    fish_state = FishingState(carmera,skill, exclamation, drag_hook)
    
    while True:
        state = fish_state.get_state()  
        print(state)