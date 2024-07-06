

import cv2
from utils.match import find_postion_by_color, rgbs2hsv

low, up = rgbs2hsv("#4AA3BA,#4CD5FE,#4CDAFF,#3BAEF5,#3BAEF5,#44C4EB,#3EB4D6,#44C8FE,#50C8E5")
image = cv2.imread("bar.png")
find_postion_by_color(image, (low, up), True)