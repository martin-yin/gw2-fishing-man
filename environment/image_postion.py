from win32 import win32gui
import cv2
from utils.match_image import match_image
from utils.utils import get_frame, get_hwnd, offset_position, real_position

class FishImagePosition:
    def __init__(self, config_position):  
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
        drag_score_position: 钓鱼分数的位置
        """
        self.skill_position = (0, 0, 0, 0)
        self.exclamation_position = (0, 0, 0, 0)
        self.drag_hook_position = (0, 0, 0, 0)
        self.drag_bar_position = (0, 0, 0, 0)
        self.drag_score_position = (0, 0, 0, 0)

        self.init_game_window()
        self.init_positions(config_position)
        frame = get_frame(self.environment_position)
        self.init_skill_position(frame)


    def init_game_window(self):
        """
        初始化游戏窗口
        """
        left, top, right, bottom = win32gui.GetWindowRect(get_hwnd())
        """ 游戏整体相对于window的位置 """
        self.environment_position = (left, top, right, bottom)
        """ 游戏的宽高 """
        self.environment_size = (right - left, bottom - top)
        """ 游戏的中心位置 """
        self.environment_center_position = (left + self.environment_size[0] // 2, top + self.environment_size[1] // 2)
    
    def init_positions(self, config_position):
        """
        初始化坐标点的位置
        """
        center_x = self.environment_center_position[0]
        center_ = self.environment_center_position[0]

        game_postion = self.environment_position
        exclamation_offset = config_position['exclamation_offset']
        drag_hook_offset = config_position['drag_hook_offset']
        drag_bar_offset = config_position['drag_bar_offset']
        drag_score_offset = config_position['drag_score_offset']
         
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
        
        self.drag_score_position = offset_position(
            (center_x, game_postion[3], center_x, game_postion[3]), 
            drag_score_offset
        )

    def init_skill_position(self, image):
        """ 初始化 钓鱼抛杆、收杆的位置"""
        position = match_image(self.skill_throw, image)

        if len(position) == 0:
            position = match_image(self.skill_collect, image)
            if len(position) == 0:
                print(f'未找到钓鱼技图标, 执行退出！')
                exit()

        game_postion = self.environment_position
        self.skill_position = real_position(game_postion, position[0])

