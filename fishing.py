import time
import cv2
from gw2_window import GW2Window
from utils.keybord import key_down, key_up, post_key_event
from utils.match_image import extract_blue_area, extract_green_area, macth_red_exclamatory, match_bar_position, match_hook, match_image
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


        self.last_bar_center_position = None
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
                print(f'未找到{self.fish_state}图标, 执行退出')
                exit()

        self.skill_position = real_position(self.gw2.position, position[0])

    def init_exclamation_position(self): 
        """ 初始化 感叹号的位置 """
        center_one = self.gw2.center_position[0]
        game_postion = self.gw2.position
        self.exclamation_position = (center_one - 60, game_postion[3] - 762, center_one + 60, game_postion[3] - 602)
    
    def init_drag_hook_position(self):
        """ 钓鱼拉扯的位置"""
        center_one = self.gw2.center_position[0]
        game_postion = self.gw2.position
        self.drag_hook_position = (center_one - 214, game_postion[3] - 452, center_one - 166, game_postion[3] - 404)
        
    def init_drag_bar_bposition(self):
        """ 拉扯条的位置"""
        center_one = self.gw2.center_position[0]
        center_two = self.gw2.center_position[1]
        game_postion = self.gw2.position
        position = (center_one - 216, game_postion[3] - 490, center_one + 216, game_postion[3] - 452)
        self.drag_bar_position = position
        

    def get_filsh_state_width_skill(self):
        """ 通过技能来判断当前的钓鱼状态 """
        skill_image = self.gw2.window_screenshot(self.skill_position)
        position = match_image(self.skill_throw, skill_image)
        if len(position) == 0:
            position = match_image(self.skill_collect, skill_image)
            if len(position) == 0:
                print(f'未找到{self.fish_state}图标，等待 2 秒后继续查找')
                time.sleep(2)
                return
            self.fish_state = "等待收杆"
            self.not_find_hook_count = 0
        else:
            self.fish_state = "等待抛杆"
            self.not_find_hook_count = 0

        print(f'当前钓鱼状态：{self.fish_state}')

    def reset_fish_state(self):
        self.get_filsh_state_width_skill()

    def drag_action(self):
        drag_hook_image = self.gw2.window_screenshot(self.drag_hook_position)
        _, hook_position = match_hook(self.drag_hook, drag_hook_image, False)
        if hook_position is None:
            self.not_find_hook_count += 1
            return 
        
        bar_image = self.gw2.window_screenshot(self.drag_bar_position)
        bar_center_box, bar_center_position = extract_green_area(bar_image, False)
        bar_box, bar_position = extract_blue_area(bar_image, False)
        if bar_center_box is None or bar_box is None:
            return
        
        bar_center_middle = (bar_center_box[0] + bar_center_box[2]) / 2
        bar_middle = (bar_box[0] + bar_box[2]) / 2

        dead_zone = 2 
        if abs(bar_center_middle - bar_middle) <= dead_zone:
            # 在死区范围内，不进行任何调整
            key_up(self.gw2.hwnd, 48 + 2)
            key_up(self.gw2.hwnd, 48 + 3)
            return

        if bar_center_middle < bar_middle - dead_zone:
            key_up(self.gw2.hwnd, 48 + 3)
            key_down(self.gw2.hwnd, 48 + 2)
         
        elif bar_center_middle > bar_middle + dead_zone:
            key_up(self.gw2.hwnd, 48 + 2)
            key_down(self.gw2.hwnd, 48 + 3)
         
            
    def fish_action(self):
        """ 钓鱼操作 """
        if self.fish_state is None:
            exit()
   
        if self.not_find_hook_count > 10:
            time.sleep(6)
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
            print(f"当前状态 {self.fish_state}")
            self.drag_action()
            return
        