from hand_class import Hand


class Hands(object):

    def __init__(self):
        self.hand_list = []

    def set_hands_class(self, multi_hand_landmarks, heigh, width):
        hand_list = []
        if multi_hand_landmarks:
            for hand_landmarks in multi_hand_landmarks:
                # mp_drawing.draw_landmarks(
                #     image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                hand = Hand(hand_landmarks.landmark, heigh, width)
                hand_list.append(hand)
        self.hand_list = hand_list

    def ishand(self):
        return self.hand_list != []
