import time
import cv2
from gw2_window import GW2Window
from utils.keybord import key_down, key_up, post_key_event
from utils.match_image import extract_blue_area, macth_red_exclamatory, match_bar_position, match_image
from utils.show_target import Show_target, real_position

class Fishing:
    def __init__(self, gw2: GW2Window):
        self.fish_throw = cv2.imread('./images/throw.png')
        self.fish_collect = cv2.imread('./images/collect.png')
        self.fish_bar_center = cv2.imread('./images/bar-center.png')

        self.fish_state = None
        # 鱼竿的位置
        self.rod_position = (0, 0, 0, 0)
        # 上鱼状态的位置
        self.hook_position = (0,0, 0, 0)
        self.drag_position = (0, 0, 0, 0)

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
        print(f'鱼竿的坐标：{self.rod_position}')

    def init_hook_position(self):
        # 游戏窗口中心点位置
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.hook_position = (center_one - 80, center_two + 50 , center_one + 80, center_two + 220)
        print(self.hook_position)

    def init_drag_position(self):
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.drag_position = (center_one - 290, center_two + 300, center_one + 290, center_two + 400)

    def get_rod_state(self):
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
        # cv2.imwrite(f'{time.time()}.png', bar_image)
        bar_center_box, bar_center_position = match_bar_position(self.fish_bar_center, bar_image)
        bar_box, bar_position = extract_blue_area(bar_image)
        if bar_position is None or bar_center_position is None:
            print("未找到拉扯框")
            return
        
        print(f'拉扯框坐标：{bar_box}')
        print(f'中心点坐标：{bar_center_box}')
        if bar_center_box[2] + 40 > bar_box[2]:
            print("中心点大于 bar_box 右侧")
            key_up(self.gw2.hwnd, 48 + 2)
            key_down(self.gw2.hwnd, 48 + 3)

        if bar_center_box[0] - 40 < bar_box[0]:
            print("中心点大于 bar_box 左侧")            
            print(bar_center_position[0], bar_box[0])            
            key_up(self.gw2.hwnd, 48 + 3)
            key_down(self.gw2.hwnd, 48 + 2)
        
    def get_fish_state(self, debug=False):
        if self.fish_state is None:
            exit()

        print(f'当前鱼竿状态：{self.fish_state}')
        if self.fish_state == "等待抛杆":
            # 抛竿操作，抛竿后等待 3 秒在继续截图
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
            print("收杆拉扯……")
            self.get_action()
            time.sleep(0.1)
            return
        return False