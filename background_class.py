import numpy as np
import cv2
from numpy.core.fromnumeric import resize


class Background(object):

    def __init__(self, img):
        self.img = img
        self.imfr_pic = 0
        self.img_pointx = 0
        self.img_pointy = 0
        self.img_absx = 0
        self.img_absy = 0
        self.move_flag = False

    def add_frame(self, fr_pic: int, color: list):
        cp_img = self.img

        bk1 = np.zeros((fr_pic, cp_img.shape[1], 3), dtype=np.int64)
        bk1[np.where((bk1 == [0, 0, 0]).all(axis=2))] = color
        array = np.insert(cp_img, 0, bk1, axis=0)
        array = np.insert(array, array.shape[0], bk1, axis=0)
        cp_img = array

        bk2 = np.zeros((array.shape[0], fr_pic, 3), dtype=np.int64)
        bk2[np.where((bk2 == [0, 0, 0]).all(axis=2))] = color
        array = np.insert(array, [0], bk2, axis=1)
        array = np.insert(array, [array.shape[1]], bk2, axis=1)
        self.img = array

        self.imfr_pic = self.imfr_pic + fr_pic

        return array

    def del_frame(self):
        if self.imfr_pic == 0:
            return 0
        else:
            array = self.img

            array = np.delete(array, np.s_[0:self.imfr_pic], 0)
            array = np.delete(
                array, np.s_[array.shape[0]-self.imfr_pic:array.shape[0]], 0)

            array = np.delete(array, np.s_[0:self.imfr_pic], 1)
            array = np.delete(
                array, np.s_[array.shape[1]-self.imfr_pic:array.shape[1]], 1)

            self.img = array
            self.imfr_pic = 0

        return array

    def ispointin(self, pointx, pointy):
        return (self.img_pointx <= pointx <= self.img_pointx + self.img.shape[1]) and (self.img_pointy <= pointy <= self.img_pointy + self.img.shape[0])

    def resize_per(self, high: int, wide: int, per: int):
        if self.img.shape[0]/high > self.img.shape[1]/wide:
            rsize = high / per
            resize_img = cv2.resize(
                self.img, (int(self.img.shape[1] * rsize / self.img.shape[0]), int(rsize)))
        else:
            rsize = wide / per
            resize_img = cv2.resize(self.img, (int(rsize), int(
                self.img.shape[0] * rsize / self.img.shape[1])))

        self.img = resize_img

        return resize_img

    def set_abspoint(self, pointx, pointy):
        self.move_flag = True
        self.img_absx = pointx
        self.img_absy = pointy

    def change_point(self, pointx, pointy, wide, high):
        self.img_pointx += pointx - self.img_absx
        self.img_pointy += pointy - self.img_absy
        self.img_absx = pointx
        self.img_absy = pointy

        if self.img_pointx < 0:
            self.img_pointx = 0
        elif self.img_pointx > wide - self.img.shape[1]:
            self.img_pointx = wide - self.img.shape[1]

        if self.img_pointy < 0:
            self.img_pointy = 0
        elif self.img_pointy > high - self.img.shape[0]:
            self.img_pointy = high - self.img.shape[0]

        pass
