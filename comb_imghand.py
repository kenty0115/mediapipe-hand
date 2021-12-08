from hand_class import comp_point


class Imhand(object):

    def __init__(self, backgounds_class: list, hands_class: list):
        self.backgounds_class = backgounds_class
        self.hands_class = hands_class

    def backgound_adhand(self):
        for backgound in self.backgounds_class:
            for i, hand in enumerate(self.hands_class):
                if i == 0:
                    backgound.hand = hand
                    continue

                im_center_x, im_center_y = backgound.center()
                if comp_point(im_center_x, im_center_y, hand.centerx, hand.centery, backgound.hand.centerx, backgound.hand.centerx) == 1:
                    backgound.hand = hand

    def set_moveflag(self):
        for backgound in self.backgounds_class:
            if backgound.ispointin(backgound.hand.centerx, backgound.hand.centery) is True:
                if backgound.hand.ishand_close() is True and backgound.move_flag is False:
                    backgound.set_abspoint(
                        backgound.hand.centerx, backgound.hand.centery)

                if backgound.move_flag is True and backgound.hand.ishand_open() is True:
                    backgound.fin_change()

    def change_backgound_point(self, heigh, width):
        hand_list = []
        img_list = self.backgounds_class.copy()
        for background in self.backgounds_class:
            if background.move_flag is True:
                hand_list.append(background.hand)
                background.change_point(
                    background.hand.centerx, background.hand.centery, width, heigh)
                img_list.remove(background)

        for background in img_list:
            if background.hand in hand_list:
                background.move_flag = False
                continue

            if background.move_flag is True:
                background.change_point(
                    background.hand.centerx, background.hand.centery, width, heigh)
                # 一つの手に2つ以上の画像を持たせないようにする処理
                hand_list.append(background.hand)
