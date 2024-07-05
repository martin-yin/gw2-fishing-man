import cv2


class Fishing:
    def __init__(self):
        # 收杆后钓力图标（用来判断是否正在跟鱼拉扯）
        self.drag_hook = cv2.imread('./images/drag_hook.png')