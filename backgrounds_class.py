import os

import cv2

from background_class import Background


class Backgrounds(object):

    def __init__(self):
        self.background_list = []
        self.fit_list = []

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
        fit_list = []
        for background in self.background_list:
            if background.move_flag is True:
                fit_list.insert(len(fit_list), background)
            else:
                fit_list.insert(0, background)
        self.fit_list = fit_list

        return fit_list

    def fit_main(self, img):
        img_a = img.copy()
        for background in self.fit_list:
            if background.move_flag is True:
                background.del_frame()
                background.add_frame(5, [0, 0, 255])
                img_a = background.comb_main(img_a)
            else:
                background.del_frame()
                background.add_frame(5, [0, 255, 0])
                img_a = background.comb_main(img_a)
        return img_a
