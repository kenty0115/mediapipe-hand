from hand_class import comp_point


class Imhand(object):

    def __init__(self, backgrounds_class: list, hand_class: object):
        self.backgrounds_class = backgrounds_class
        self.hand_class = hand_class

    def background_adhand(self):
        for background in self.backgrounds_class:
            background.hand = self.hand_class
            # for i, hand in enumerate(self.hands_class):
            #     if i == 0:
            #         background.hand = hand
            #         continue

            #     im_center_x, im_center_y = background.center()
            #     if comp_point(im_center_x, im_center_y, hand.centerx, hand.centery, background.hand.centerx, background.hand.centerx) == 1:
            #         background.hand = hand

    def set_moveflag(self):
        flag = False
        for background in self.backgrounds_class:
            if background.move_flag is True:
                if background.hand.ishand_open() is True:
                    background.fin_change()
                flag = True
                break

        if flag is False:
            for background in self.backgrounds_class:
                if background.ispointin(background.hand.centerx, background.hand.centery) is True:
                    if background.hand.ishand_close() is True and background.move_flag is False:
                        background.set_abspoint(
                            background.hand.centerx, background.hand.centery)
                        break

                    if background.move_flag is True and background.hand.ishand_open() is True:
                        background.fin_change()

    def change_background_point(self):
        for background in self.backgrounds_class:
            if background.move_flag is True:
                background.change_point(
                    background.hand.centerx, background.hand.centery)
                break
