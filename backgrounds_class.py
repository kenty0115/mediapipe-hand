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

    # def set_imgs_class(self, path: str, heigh, width, tate, yoko):
    #     list_a = []
    #     file_list = os.listdir(path)
    #     root, ext = os.path.splitext(file_list[0])
    #     print(file_list)
    #     if ext == '.png' or '.jpeg' or '.jpg':
    #         abs_name = path + '/' + file_list[0]
    #         image = cv2.imread(abs_name)
    #         h = image.shape[0]
    #         w = image.shape[1]
    #         print(image.shape)
    #         ha = int(h / yoko + 1)
    #         wa = int(w / tate + 1)
    #         print(wa)
    #         for hi in range(yoko + 1):
    #             hi = hi * ha
    #             print(f"hi:{hi}")
    #             for wi in range(tate + 1):
    #                 wi = wi * wa
    #                 print(f"wi:{wi}")
    #                 image_a = image[hi:hi + ha, wi:wi + wa]
    #                 list_a.append(Background(image_a, width, heigh))

    #     self.background_list = list_a

    def resize_per(self, heigh: int, width: int,  per: int):
        for background in self.background_list:
            print(background)
            background.resize_per(heigh, width, per)
            print("a")

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
