import mediapipe as mp
import cv2

from hand_class import Hand
from backgrounds_class import Backgrounds
from comb_imghand import Imhand


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.hands

obj_per = 3
img_path = "./img/"
backgrounds_class = Backgrounds()
backgrounds_class.set_imgs_class(img_path)

first_loop = True
cap = cv2.VideoCapture(0)
with mp_holistic.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        width = image.shape[1]
        heigh = image.shape[0]

        if first_loop is True:
            first_loop = False
            print(image.shape)
            backgrounds_class.resize_per(heigh, width, obj_per)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_list = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                hand = Hand(hand_landmarks.landmark, heigh, width)
                hand_list.append(hand)

        imhand = Imhand(backgrounds_class.background_list, hand_list)

        near_index = []
        if hand_list != []:

            imhand.backgound_adhand()

            imhand.set_moveflag()
            imhand.change_backgound_point(heigh, width)

        backgrounds_class.set_fitlist()

        image = backgrounds_class.fit_main(image)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
