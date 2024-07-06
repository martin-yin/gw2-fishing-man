import time
import cv2
from win32 import win32gui
import ctypes
from environment.image_postion import FishPosition
from utils.match_image import match_image
from utils.utils import key_down, key_up

""" 钓鱼环境 """
class DQNFishing:
    def __int___(self, postion: FishPosition):
        self.fish_state = None
        # self.camera = Camera()
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
