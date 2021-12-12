import numpy as np
import cv2


class Background(object):

    def __init__(self, img, width, heigh):
        self.img = img
        self.main_width = width
        self.main_heigh = heigh
        self.fr_pic = 0
        self.point_x = 0
        self.point_y = 0
        self.abs_x = 0
        self.abs_y = 0
        self.move_flag = False
        self.hand = None

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

        self.fr_pic = self.fr_pic + fr_pic

        return array

    def del_frame(self):
        if self.fr_pic == 0:
            return 0
        else:
            array = self.img

            array = np.delete(array, np.s_[0:self.fr_pic], 0)
            array = np.delete(
                array, np.s_[array.shape[0]-self.fr_pic:array.shape[0]], 0)

            array = np.delete(array, np.s_[0:self.fr_pic], 1)
            array = np.delete(
                array, np.s_[array.shape[1]-self.fr_pic:array.shape[1]], 1)

            self.img = array
            self.fr_pic = 0

        return array

    def ispointin(self, pointx, pointy):
        return (self.point_x <= pointx <= self.point_x + self.img.shape[1]) and (self.point_y <= pointy <= self.point_y + self.img.shape[0])

    def resize_per(self, heigh: int, width: int, per: int):
        if self.img.shape[0]/heigh > self.img.shape[1]/width:
            rsize = heigh / per
            resize_img = cv2.resize(
                self.img, (int(self.img.shape[1] * rsize / self.img.shape[0]), int(rsize)))
        else:
            rsize = width / per
            resize_img = cv2.resize(self.img, (int(rsize), int(
                self.img.shape[0] * rsize / self.img.shape[1])))

        self.img = resize_img

        return resize_img

    def set_abspoint(self, pointx, pointy):
        self.move_flag = True
        self.abs_x = pointx
        self.abs_y = pointy

    def change_point(self, pointx, pointy):
        self.point_x += pointx - self.abs_x
        self.point_y += pointy - self.abs_y
        self.abs_x = pointx
        self.abs_y = pointy

        if self.point_x < 0:
            self.point_x = 0
        elif self.point_x > self.main_width - self.img.shape[1]:
            self.point_x = self.main_width - self.img.shape[1]

        if self.point_y < 0:
            self.point_y = 0
        elif self.point_y > self.main_heigh - self.img.shape[0]:
            self.point_y = self.main_heigh - self.img.shape[0]

    def fin_change(self):
        self.move_flag = False
        self.abs_x = 0
        self.abs_y = 0

    def center(self):
        return self.point_x + int(self.img.shape[1]/2), self.point_y + int(self.img.shape[0]/2)

    def comb_main(self, image):
        image[self.point_y:self.point_y+self.img.shape[0],
              self.point_x:self.point_x+self.img.shape[1]] = self.img
        return image
