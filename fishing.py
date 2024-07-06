import time
import cv2
from utils.match import  find_postion_by_color, match_image, rgbs2hsv
from utils.utils import get_frame, get_hwnd, key_down, key_down_up, key_up

class Fishing:
    def __init__(self, skill_position, exclamation_position, drag_hook_position, drag_bar_position):
        self.drag_bar_position = drag_bar_position
        """钓鱼抛杆的图标"""
        self.skill_throw = cv2.imread('./images/skill_throw.png', cv2.IMREAD_GRAYSCALE)
        """钓鱼收杆的图标"""
        self.skill_collect = cv2.imread('./images/skill_collect.png', cv2.IMREAD_GRAYSCALE)
        """收杆后钓力图标（用来判断是否正在跟鱼拉扯）"""
        self.drag_hook = cv2.imread('./images/drag_hook.png', cv2.IMREAD_GRAYSCALE)

        self.skill_position = skill_position
        self.exclamation_position = exclamation_position
        self.exclamatory_colors = rgbs2hsv("#5032F7,#4E2EE2,#6C35FB,#8731FB,#5D26DD,#6625C8,#4A30DE,#5D1AA1,#461767")
        self.drag_bar_center_colors = rgbs2hsv("#4DC663,#56E77F,#54FA88,#76FAA0,#76FEAA,#69F898,#4CFA98,#49F298,#6EFF76,#5EEF72")
        self.drag_bar_box_colors = rgbs2hsv("#4AA3BA,#4CD5FE,#4CDAFF,#3BAEF5,#3BAEF5,#44C4EB,#3EB4D6,#44C8FE,#50C8E5")

        self.drag_hook_position = drag_hook_position
        self.state = None
        self.not_find_hook_count = 0
        
    def reset(self):
        """ 通过技能来判断当前的钓鱼状态 """
        time.sleep(2)
        skill_image = get_frame(self.skill_position)
        position = match_image(self.skill_collect, skill_image)
        if position is None:
            position = match_image(self.skill_throw, skill_image)
            if position is None:
                exit("未找到钓鱼技能")
            else:
                key_down_up(get_hwnd(), 48 + 1)
                time.sleep(2)
                self.state = 1

        self.state = 1
        self.not_find_hook_count = 0

    def get_state(self):
        """ 0: 抛竿操作
            1: 等待鱼上钩
            2: 鱼上钩了拉扯
        """
        print('当前状态：', self.state)
        if self.not_find_hook_count >= 30:
            print('重新获取钓鱼状态')
            self.reset()
            return
        
        if self.state == 1:
            exclamatory = get_frame(self.exclamation_position)
            red_exclamatory = find_postion_by_color(exclamatory, self.exclamatory_colors)
            if red_exclamatory is not None:
                self.state = 2
                key_down_up(get_hwnd(), 48 + 1)
                time.sleep(0.05)
                return
            time.sleep(0.5)
        
        if self.state == 2:
            """ 在执行拉扯的操作 """
            tempalte = get_frame(self.drag_hook_position)
            hook_position = match_image(self.drag_hook, tempalte)
            if hook_position is None:
                self.not_find_hook_count += 1
                print('未找到鱼钩图标')


    def drag_action(self):
        hwnd = get_hwnd()
        bar_image = get_frame(self.drag_bar_position)
        bar_center_box  = find_postion_by_color(bar_image, self.drag_bar_center_colors)
        bar_box = find_postion_by_color(bar_image,self.drag_bar_box_colors)
        if bar_center_box is None or bar_box is None:
            return
        
        bar_center_middle = (bar_center_box[0] + bar_center_box[2]) / 2
        bar_middle = (bar_box[0] + bar_box[2]) / 2
        dead_zone = 6

        if abs(bar_center_middle - bar_middle) <= dead_zone:
            # 在死区范围内，不进行任何调整
            key_up(hwnd, 48 + 2)
            key_up(hwnd, 48 + 3)
            return

        if bar_center_middle < bar_middle - dead_zone:
            key_up(hwnd, 48 + 3)
            key_down(hwnd, 48 + 2)
         
        elif bar_center_middle > bar_middle + dead_zone:
            key_up(hwnd, 48 + 2)
            key_down(hwnd, 48 + 3)
         
            