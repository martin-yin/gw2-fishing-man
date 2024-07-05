
import time
import cv2

from utils.match_image import macth_red_exclamatory, match_hook, match_image
from utils.utils import Camera, key_down_up

class FishingState:
    def __init__(self, hwnd, carmera: Camera, skill_position, exclamation_position, drag_hook_position):
        self.carmera = carmera
        """钓鱼抛杆的图标"""
        self.skill_throw = cv2.imread('./images/skill_throw.png', cv2.IMREAD_GRAYSCALE)
        """钓鱼收杆的图标"""
        self.skill_collect = cv2.imread('./images/skill_collect.png', cv2.IMREAD_GRAYSCALE)
        """收杆后钓力图标（用来判断是否正在跟鱼拉扯）"""
        self.drag_hook = cv2.imread('./images/drag_hook.png', cv2.IMREAD_GRAYSCALE)
        self.hwnd = hwnd
        self.skill_position = skill_position
        self.exclamation_position = exclamation_position
        self.drag_hook_position = drag_hook_position
        self.fish_state = None
        self.not_find_hook_count = 0

        self.reset()

    def reset(self):
        """ 通过技能来判断当前的钓鱼状态 """
        time.sleep(3)
        skill_image = self.carmera.get_frame(self.skill_position)
        position = match_image(self.skill_collect, skill_image)
        if len(position) == 0:
            position = match_image(self.skill_throw, skill_image)
            if len(position) == 0:
                exit("未找到钓鱼技能")
            else:
                key_down_up(self.hwnd, 48 + 1)
                time.sleep(4)
                self.fish_state = 1

        self.fish_state = 1
        self.not_find_hook_count = 0

    def get_state(self):
        """ 0: 抛竿操作
            1: 等待鱼上钩
            2: 鱼上钩了拉扯
        """
        if self.not_find_hook_count >= 30:
            print('重新获取钓鱼状态')
            self.reset()
            return
        
        if self.fish_state == 1:
            exclamatory = self.carmera.get_frame(self.exclamation_position)
            red_exclamatory = macth_red_exclamatory(exclamatory)
            if red_exclamatory:
                self.fish_state = 2
                key_down_up(self.hwnd, 48 + 1)
                time.sleep(1)
        
        if self.fish_state == 2:
            """ 在执行拉扯的操作 """
            tempalte = self.carmera.get_frame(self.drag_hook_position)
            _, hook_position = match_hook(self.drag_hook, tempalte, False)
            if hook_position is None:
                self.not_find_hook_count += 1
                print('未找到钩子')

        return self.fish_state