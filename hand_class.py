from point_def import comp_point


class Hand(object):

    def __init__(self, landmark: list, heigh, width):
        self.landmark = landmark
        self.heigh = heigh
        self.width = width
        self.point_list = self.hand_point()
        self.centerx, self.centery = self.hand_center()
        self.hand_num = self._hand_num()

    def hand_point(self):
        point_list = [(int(self.width * landmark.x), int(self.heigh * landmark.y))
                      for landmark in self.landmark]

        self.hand_point = point_list
        return point_list

    def hand_center(self):
        return int((self.point_list[0][0]+self.point_list[9][0]) /
                   2), int((self.point_list[0][1] + self.point_list[9][1])/2)

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
