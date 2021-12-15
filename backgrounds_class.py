import os
from collections import deque

import cv2

from background_class import Background


class Backgrounds(object):

    def __init__(self):
        self.background_list = []
        self.fit_que = None

    def set_imgs_class(self, path: str, heigh, width):
        list_a = []
        file_list = os.listdir(path)
        for file_name in file_list:
            root, ext = os.path.splitext(file_name)
            if ext == '.png' or '.jpeg' or '.jpg':
                abs_name = path + '/' + file_name
                image = cv2.imread(abs_name)
                list_a.append(Background(image, width, heigh))

        self.background_list = list_a

    def resize_per(self, heigh: int, width: int,  per: int):
        for background in self.background_list:
            background.resize_per(heigh, width, per)

    def set_fitlist(self):
        fit_que = deque()
        for background in self.background_list:
            if background.move_flag is True:
                fit_que.append(background)
            else:
                fit_que.appendleft(background)
        self.fit_que = fit_que

        return fit_que

    def fit_main(self, img):
        img_a = img.copy()
        for background in self.fit_que:
            if background.move_flag is True:
                color = [0, 0, 255]
                background.set_frcolor(color, 5)
                img_a = background.comb_main(img_a)
            else:
                color = [0, 255, 0]
                background.set_frcolor(color, 5)
                img_a = background.comb_main(img_a)
        return img_a
