import time
import cv2
from win32 import win32api, win32gui, win32print
import ctypes
from utils.keybord import key_down, key_up
from utils.match_image import match_image
from utils.show_target import offset_position, position_border_draw, real_position
import dxcam

class Camera: 
    def __init__(self):
        self.camera = dxcam.create()
# class DQNFishingEnvironment:
#     def __init__(self, show_postion = False, exclamation_offset = (-60, -762, 60, -602), drag_hook_offset =  (-214, -452, -166, -404), drag_bar_offset =  (-216, -490, 216, -452)):
#         """钓鱼抛杆的图标"""
#         self.skill_throw = cv2.imread('./images/skill_throw.png', cv2.IMREAD_GRAYSCALE)
#         """钓鱼收杆的图标"""
#         self.skill_collect = cv2.imread('./images/skill_collect.png', cv2.IMREAD_GRAYSCALE)
#         """收杆后钓力图标（用来判断是否正在跟鱼拉扯）"""
#         self.drag_hook = cv2.imread('./images/drag_hook.png', cv2.IMREAD_GRAYSCALE)

#         """ 环境的窗口句柄 """
#         self.hwnd = None
#         """ 环境的位置、大小、中心位置 """
#         self.environment_position = (0, 0, 0, 0)
#         self.environment_size = (0, 0)
#         self.environment_center_position = (0, 0)

#         """ 
#         四个坐标点的位置
#         skill_position: 技能图标的位置
#         exclamation_position: 钓鱼提示图标的位置
#         drag_hook_position: 钓力图标的位置  
#         drag_bar_position: 钓力条的位置
#         """
#         self.skill_position = (0, 0, 0, 0)
#         self.exclamation_position = (0, 0, 0, 0)
#         self.drag_hook_position = (0, 0, 0, 0)
#         self.drag_bar_position = (0, 0, 0, 0)

#         """ 钓鱼状态 """
#         self.fish_state = None

#         self.init_game_window()
#         self.init_positions(show_postion, exclamation_offset, drag_hook_offset, drag_bar_offset)

#     def init_game_window(self):
#         """
#         初始化游戏窗口
#         """
#         user32 = ctypes.windll.user32
#         user32.GetDpiForSystem()
#         self.hwnd = win32gui.FindWindow(None, "激战2")
#         left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
#         """ 游戏整体相对于window的位置 """
#         self.environment_position = (left, top, right, bottom)
#         """ 游戏的宽高 """
#         self.environment_size = (right - left, bottom - top)
#         """ 游戏的中心位置 """
#         self.environment_center_position = (left + self.environment_size[0] // 2, top + self.environment_size[1] // 2)
  
#     def init_positions(self, show_postion = False, exclamation_offset = (-60, -762, 60, -602), drag_hook_offset =    (-214, -452, -166, -404), drag_bar_offset =  (-216, -490, 216, -452)):
#         """
#         初始化坐标点的位置
#         """
#         center_x = self.environment_center_position[0]
#         game_postion = self.environment_position
        
#         self.exclamation_position = offset_position(
#             (center_x, game_postion[3], center_x, game_postion[3]), 
#             exclamation_offset
#         )

#         self.drag_hook_position = offset_position(
#             (center_x, game_postion[3], center_x, game_postion[3]), 
#            drag_hook_offset
#         )

#         self.drag_bar_position = offset_position(
#             (center_x, game_postion[3], center_x, game_postion[3]), 
#             drag_bar_offset
#         )

#         if show_postion is True:
#             position_border_draw(self.hwnd, self.exclamation_position)
#             position_border_draw(self.hwnd, self.drag_hook_position)
#             position_border_draw(self.hwnd, self.drag_bar_position)

        
#     def init_skill_position(self, image):
#         """ 初始化 钓鱼抛杆、收杆的位置"""
#         position = match_image(self.skill_throw, image)
#         if len(position) == 0:
#             position = match_image(self.skill_collect, image)
#             if len(position) == 0:
#                 print(f'未找到{self.fish_state}图标, 执行退出')
#                 exit()

#         game_postion = self.environment_position
#         skill_position = real_position(game_postion, position)

#         return skill_position


class FishPosition:
    def __init__(self, hwnd, exclamation_offset = (-60, -762, 60, -602), drag_hook_offset =  (-214, -452, -166, -404), drag_bar_offset =  (-216, -490, 216, -452)): 
        """钓鱼抛杆的图标"""
        self.skill_throw = cv2.imread('./images/skill_throw.png', cv2.IMREAD_GRAYSCALE)
        """钓鱼收杆的图标"""
        self.skill_collect = cv2.imread('./images/skill_collect.png', cv2.IMREAD_GRAYSCALE)
        """收杆后钓力图标（用来判断是否正在跟鱼拉扯）"""
        self.drag_hook = cv2.imread('./images/drag_hook.png', cv2.IMREAD_GRAYSCALE)
        """ 环境的位置、大小、中心位置 """
        self.environment_position = (0, 0, 0, 0)
        self.environment_size = (0, 0)
        self.environment_center_position = (0, 0)

        """ 
        四个坐标点的位置
        skill_position: 技能图标的位置
        exclamation_position: 钓鱼提示图标的位置
        drag_hook_position: 钓力图标的位置  
        drag_bar_position: 钓力条的位置
        """
        self.skill_position = (0, 0, 0, 0)
        self.exclamation_position = (0, 0, 0, 0)
        self.drag_hook_position = (0, 0, 0, 0)
        self.drag_bar_position = (0, 0, 0, 0)

        self.init_game_window(hwnd)
        self.init_positions(exclamation_offset, drag_hook_offset, drag_bar_offset)
        self.init_skill_position()


    def init_game_window(self, hwnd):
        """
        初始化游戏窗口
        """
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        """ 游戏整体相对于window的位置 """
        self.environment_position = (left, top, right, bottom)
        """ 游戏的宽高 """
        self.environment_size = (right - left, bottom - top)
        """ 游戏的中心位置 """
        self.environment_center_position = (left + self.environment_size[0] // 2, top + self.environment_size[1] // 2)
    
    def init_positions(self, exclamation_offset, drag_hook_offset, drag_bar_offset):
        """
        初始化坐标点的位置
        """
        center_x = self.environment_center_position[0]
        game_postion = self.environment_position
        
        self.exclamation_position = offset_position(
            (center_x, game_postion[3], center_x, game_postion[3]), 
            exclamation_offset
        )

        self.drag_hook_position = offset_position(
            (center_x, game_postion[3], center_x, game_postion[3]), 
           drag_hook_offset
        )

        self.drag_bar_position = offset_position(
            (center_x, game_postion[3], center_x, game_postion[3]), 
            drag_bar_offset
        )

    def init_skill_position(self, image):
        """ 初始化 钓鱼抛杆、收杆的位置"""
        position = match_image(self.skill_throw, image)
        if len(position) == 0:
            position = match_image(self.skill_collect, image)
            if len(position) == 0:
                print(f'未找到{self.fish_state}图标, 执行退出')
                exit()

        game_postion = self.environment_position
        skill_position = real_position(game_postion, position)

        return skill_position

""" 钓鱼环境 """
class DQNFishing:
    def __int___(self, postion: FishPosition):
        self.fish_state = None
        self.camera = Camera().camera
        self.postion = postion
    
    """ 开始新一轮的钓鱼"""
    def reset(self):
        return self.get_state()

    def get_state(self):
        """ 获取当前拖拽的状态"""
        return self.camera.grab(region=self.postion.drag_bar_position)

    """ 返回 当前状态 和 分数 """
    def step(self, action):
        self.do_action(action)
        time.sleep(0.01)
        # 计算分数
        score = 0
        print(f"本轮分数: {score}")
        return self.get_state(), score

    """ 执行动作 """
    def do_action(self, hwnd, action):
        if action == 0:
            key_up(hwnd, 48 + 2)
            key_up(hwnd, 48 + 3)
        if action == 1:
            key_up(hwnd, 48 + 3)
            key_down(hwnd, 48 + 2)
        if action == 2:
            key_up(hwnd, 48 + 3)
            key_down(hwnd, 48 + 2)
