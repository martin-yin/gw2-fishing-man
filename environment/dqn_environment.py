import time
import cv2
from win32 import win32gui
import ctypes
from environment.image_postion import FishPosition
from utils.match_image import get_score_width, match_image
from utils.utils import get_frame, key_down, key_up

""" 钓鱼环境 """
class DQNFishing:
    def __int___(self,  drag_bar_position, drag_score_position):
        self.drag_bar_position = drag_bar_position
        self.drag_score_position = drag_score_position

    def get_state(self):
        """ 获取当前拖拽的状态"""
        return get_frame(self.drag_bar_position)

    """ 返回 当前状态, 奖励分数 和 是否结束 """
    def step(self, action):
        self.do_action(action)
        time.sleep(0.01)
        # 计算分数
        score_frame = get_frame(self.drag_score_position)
        width = get_score_width(score_frame)

        if width is None:
            return self.get_state(), 0
        
        score = round(width / 318  * 100, 2)
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
