import numpy as np


# 点A(ax, ay)から点B(bx, by)と点C(cx, cy)を比べて点Bの方が近くの時1を返す。その他0
def comp_point(ax, ay, bx, by, cx, cy):
    a = np.array((ax, ay))
    b = np.array((bx, by))
    c = np.array((cx, cy))
    if np.linalg.norm(a-b) < np.linalg.norm(a-c):
        return 1
    else:
        return 0


class Hand(object):

    def __init__(self, landmark: list, wide, high):
        self.landmark = landmark
        self.wide = wide
        self.high = high
        self.point_list = self.hand_point()
        self.centerx, self.centery = self.hand_center()
        self.hand_num = self._hand_num()

    def hand_point(self):
        point_list = []
        for landmark in self.landmark:
            x_point = int(self.wide * landmark.x)
            y_point = int(self.high * landmark.y)
            point_list.append((x_point, y_point))

        self.hand_point = point_list
        return point_list

    def hand_center(self):
        return int((self.point_list[0][0]+self.point_list[9][0])/2), int((self.point_list[0][1] + self.point_list[9][1])/2)

    def ishand_open(self):
        return self.hand_num == 4

    def ishand_close(self):
        return self.hand_num == 0

    def _hand_num(self):
        cnt = 4
        # 人差し指
        index = 8
        cnt -= comp_point(self.centerx, self.centery,
                          self.hand_point[index][0], self.hand_point[index][1], self.hand_point[index - 2][0], self.hand_point[index - 2][1])
        # 中指
        index = 12
        cnt -= comp_point(self.centerx, self.centery,
                          self.hand_point[index][0], self.hand_point[index][1], self.hand_point[index - 2][0], self.hand_point[index - 2][1])
        # 薬指
        index = 16
        cnt -= comp_point(self.centerx, self.centery,
                          self.hand_point[index][0], self.hand_point[index][1], self.hand_point[index - 2][0], self.hand_point[index - 2][1])
        # 小指
        index = 20
        cnt -= comp_point(self.centerx, self.centery,
                          self.hand_point[index][0], self.hand_point[index][1], self.hand_point[index - 2][0], self.hand_point[index - 2][1])
        return cnt
