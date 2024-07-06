import time
import cv2
from win32gui import FindWindow, SetForegroundWindow
from environment.image_postion import FishImagePosition
from environment.state import FishingState
from fishing import Fishing
from utils.utils import get_frame, get_hwnd, load_config, position_border_draw

if __name__ == '__main__':
    hwnd = get_hwnd()
    SetForegroundWindow(hwnd)
    time.sleep(1)
    config = load_config("./config.yaml")
    # 获取图标位置
    fish_image_positon = FishImagePosition(config['position'])
    # skill = fish_image_positon.skill_position
    # exclamation = fish_image_positon.exclamation_position
    # drag_hook = fish_image_positon.drag_hook_position
    # drag_bar_position = fish_image_positon.drag_bar_position
    # fish_state = FishingState(skill, exclamation, drag_hook)
    # fishing = Fishing(drag_bar_position)
    print("开始钓鱼")
    while True:
        time.sleep(0.1)
        # state = fish_state.get_state()  
        # if state == 1:
        #     print("等待鱼儿上钩")
        #     time.sleep(0.5)
            
        # if state == 2:
        #     fishing.do_action()
        