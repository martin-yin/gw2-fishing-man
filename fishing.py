import time
import cv2
from gw2_window import GW2Window
from utils.keybord import key_down, key_up, post_key_event
from utils.match_image import extract_blue_area, macth_red_exclamatory, match_bar_position, match_hook, match_image
from utils.show_target import Show_target, real_position

class Fishing:
    def __init__(self, gw2: GW2Window):
        # 钓鱼状态
        self.fish_state = None

        """ 图标 """
        # 钓鱼抛杆的图标
        self.skill_throw = cv2.imread('./images/skill_throw.png')
        # 钓鱼收杆的图标
        self.skill_collect = cv2.imread('./images/skill_collect.png')
        # 收杆后钓力图标（用来判断是否正在跟鱼拉扯）
        self.drag_hook = cv2.imread('./images/drag_hook.png')
        # 钓鱼拉扯中的绿色图标
        self.drag_bar_center = cv2.imread('./images/drag_bar_center.png')

        """图标位置"""
        self.skill_position = (0, 0, 0, 0)
        self.exclamation_position = (0, 0, 0, 0)

        """ 没有找到鱼钩的次数 """
        self.not_find_hook_count = 0
        """ 其他基本 """
        self.gw2 = gw2
        self.gw2.acitvation_window()
        time.sleep(0.2)

    def init_position(self):
        """ 初始化 钓鱼抛杆、收杆、钓鱼拉扯的位置"""
        self.init_skill_position(self.gw2.window_screenshot())
        self.init_exclamation_position()
        self.init_drag_hook_position()
        self.init_drag_bar_bposition()

    def init_skill_position(self, image):
        """ 初始化 钓鱼抛杆、收杆的位置"""
        position = match_image(self.skill_throw, image)
        if len(position) == 0:
            position = match_image(self.skill_collect, image)
            if len(position) == 0:
                print(f'未找到{self.fish_state}图标')
                exit()

        self.skill_position = real_position(self.gw2.position, position[0])

    def init_exclamation_position(self): 
        """ 初始化 感叹号的位置 """
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.exclamation_position = (center_one - 80, center_two + 50 , center_one + 80, center_two + 220)
    

    def init_drag_hook_position(self):
        """ 钓鱼拉扯的位置"""
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.drag_hook_position = (center_one - 214, center_two + 392, center_one - 166, center_two + 440)
        
    def init_drag_bar_bposition(self):
        """ 拉扯条的位置"""
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        self.drag_bar_position = (center_one - 216, center_two + 354, center_one + 216, center_two + 390)
        

    def get_filsh_state_width_skill(self):
        """ 通过技能来判断当前的钓鱼状态 """
        self.not_find_hook_count = 0
        skill_image = self.gw2.window_screenshot(self.skill_position)
        position = match_image(self.skill_throw, skill_image)
        if len(position) == 0:
            position = match_image(self.skill_collect, skill_image)
            if len(position) == 0:
                print(f'未找到{self.fish_state}图标')
            self.fish_state = "等待收杆"
        else:
            self.fish_state = "等待抛杆"

    def reset_fish_state(self):
        self.get_filsh_state_width_skill()

    def drag_action(self):
        drag_hook_image = self.gw2.window_screenshot(self.drag_hook_position)
        _, hook_position = match_hook(self.drag_hook, drag_hook_image, False)
        if hook_position is None:
            self.not_find_hook_count += 1
            return 
        
        bar_image = self.gw2.window_screenshot(self.drag_bar_position)
        bar_center_box, bar_center_position = match_bar_position(self.drag_bar_center, bar_image)

        bar_box, bar_position = extract_blue_area(bar_image, False)
        if bar_position is None or bar_center_position is None:
            return
        
        self.not_find_bar_count = 0
        if bar_center_box[2] + 10 > bar_box[2]:
            key_up(self.gw2.hwnd, 48 + 2)
            key_down(self.gw2.hwnd, 48 + 3)

        if bar_center_box[0] - 10 < bar_box[0]:
            key_up(self.gw2.hwnd, 48 + 3)
            key_down(self.gw2.hwnd, 48 + 2)

    def fish_action(self):
        """ 钓鱼操作 """
        if self.fish_state is None:
            exit()
        print(f"当前{self.fish_state}状态")
        
        if self.not_find_hook_count > 10:
            time.sleep(2)
            self.reset_fish_state()
            print('重新获取钓鱼状态')

        if self.fish_state == "等待抛杆":
            post_key_event(self.gw2.hwnd, 48 + 1)
            self.fish_state = "等待收杆"
            time.sleep(3)
            return 
        if self.fish_state == "等待收杆":
            red_exclamatory = macth_red_exclamatory(self.gw2.window_screenshot(self.exclamation_position))
            if red_exclamatory:
                self.fish_state = "收杆拉扯"
                post_key_event(self.gw2.hwnd, 48 + 1)
            time.sleep(0.3)
            return
        
        if  self.fish_state == "收杆拉扯":
            self.drag_action()
            time.sleep(0.1)
            return
