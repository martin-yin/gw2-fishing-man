import time
import cv2
from gw2_window import GW2Window
from utils.keybord import key_down, key_up, post_key_event
from utils.match_image import extract_blue_area, macth_red_exclamatory, match_bar_position, match_hook, match_image
from utils.show_target import Show_target, real_position

class Fishing:
    def __init__(self, gw2: GW2Window):
        self.fish_throw = cv2.imread('./images/throw.png')
        self.fish_collect = cv2.imread('./images/collect.png')
        self.fish_bar_center = cv2.imread('./images/bar-center.png')
        self.fish_bar_hook = cv2.imread('./images/bar-hook.png')
        
        self.fish_state = None
        # 鱼竿的位置
        self.rod_position = (0, 0, 0, 0)
        # 上鱼状态的位置
        self.hook_position = (0,0, 0, 0)
        self.drag_position = (0, 0, 0, 0)

        self.not_find_bar_count = 0
        self.gw2 = gw2
        self.gw2.acitvation_window()
        time.sleep(0.5)

    def init_position(self):

        self.init_rod_position(self.gw2.window_screenshot())
        self.init_hook_position()
        self.init_drag_position()

    def init_rod_position(self, image):
        position = match_image(self.fish_throw, image)
        if len(position) == 0:
            position = match_image(self.fish_collect, image)
            if len(position) == 0:
                print(f'未找到{self.fish_state}图标')
                exit()

        self.rod_position = real_position(self.gw2.position, position[0])

    def init_hook_position(self):
        # 游戏窗口中心点位置
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.hook_position = (center_one - 80, center_two + 50 , center_one + 80, center_two + 220)

    def init_drag_position(self):
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.drag_position = (center_one - 216, center_two + 354, center_one + 216, center_two + 390)

    def get_rod_state(self):
        self.not_find_bar_count = 0
        rod_image = self.gw2.window_screenshot(self.rod_position)
        position = match_image(self.fish_throw, rod_image)
        if len(position) == 0:
            position = match_image(self.fish_collect, rod_image)
            if len(position) == 0:
                print(f'未找到{self.fish_state}图标')
            self.fish_state = "等待收杆"
        else:
            self.fish_state = "等待抛杆"

    def reset_fish_state(self):
        self.get_rod_state()


    def get_action(self):
        bar_image = self.gw2.window_screenshot(self.drag_position)
        # _, hook_position = match_hook(self.fish_bar_hook, bar_image, False)

        # if hook_position is None:
        #     self.not_find_bar_count += 1
        #     return 
        bar_center_box, bar_center_position = match_bar_position(self.fish_bar_center, bar_image)
        bar_box, bar_position = extract_blue_area(bar_image, True)
        print(f"bar_center_position:{bar_center_position}, bar_position:{bar_position}")

        if bar_position is None or bar_center_position is None:
            return
        self.not_find_bar_count = 0
        if bar_center_box[2] + 30 > bar_box[2]:
            key_up(self.gw2.hwnd, 48 + 2)
            key_down(self.gw2.hwnd, 48 + 3)

        if bar_center_box[0] - 30 < bar_box[0]:
            key_up(self.gw2.hwnd, 48 + 3)
            key_down(self.gw2.hwnd, 48 + 2)
        
    def get_fish_state(self, debug=False):
        if self.fish_state is None:
            exit()

        print(f"当前{self.fish_state}状态")

        if self.not_find_bar_count > 10:
            time.sleep(4)
            self.reset_fish_state()
            print('重置状态！')
            return
        
        if self.fish_state == "等待抛杆":
            self.fish_state = "等待收杆"
            post_key_event(self.gw2.hwnd, 48 + 1)
            time.sleep(3)
            return 
        if self.fish_state == "等待收杆":
            red_exclamatory = macth_red_exclamatory(self.gw2.window_screenshot(self.hook_position))
            if red_exclamatory:
                self.fish_state = "收杆拉扯"
                post_key_event(self.gw2.hwnd, 48 + 1)
            time.sleep(0.3)
            return
        
        if  self.fish_state == "收杆拉扯":
            self.get_action()
            time.sleep(0.1)
            return
        
        return False