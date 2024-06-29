import time
import cv2
import numpy as np
from fishing import Fishing
from gw2_window import GW2Window
from PIL import Image

from utils.show_target import Show_target
# from utils.show_target import Show_target
if __name__ == '__main__':
    gw2 = GW2Window()
    fish = Fishing(gw2)
    fish.init_position()
    fish.reset_fish_state()
    while True:
        fish.fish_action()
        # Show_target(fish.skill_position)
        # Show_target(fish.exclamation_position)
        # Show_target(fish.drag_bar_position)
        # Show_target(fish.drag_hook_position)
        
        