import mediapipe as mp
import cv2

from hand_class import Hand
from backgrounds_class import Backgrounds
from comb_imghand import Imhand

import time

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.hands

obj_per = 3
img_path = "./img/"

foucrr = cv2.VideoWriter_fourcc(*'XVID')

first_loop = True
cv2.namedWindow('MediaPipe Hand', cv2.WINDOW_AUTOSIZE)
# cv2.setWindowProperty(
#     'MediaPipe Hand', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cap = cv2.VideoCapture(0)
with mp_holistic.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # cap.set(cv2.CAP_PROP_FPS, 10)
        heigh = image.shape[0]
        width = image.shape[1]

        if first_loop is True:
            first_loop = False
            video = cv2.VideoWriter('test1.avi', foucrr, 30, (width, heigh))
            print(image.shape)
            backgrounds_class = Backgrounds()
            backgrounds_class.set_imgs_class(img_path, heigh, width)
            backgrounds_class.resize_per(heigh, width, obj_per)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_class = None
        if results.multi_hand_landmarks:
            hand_class = Hand(
                results.multi_hand_landmarks[0].landmark, heigh, width)

        if hand_class != None:

            imhand = Imhand(backgrounds_class.background_list, hand_class)
            imhand.background_adhand()
            imhand.set_moveflag()
            imhand.change_background_point()

        backgrounds_class.set_fitlist()

        # t1 = time.time()

        image = backgrounds_class.fit_main(image)

        # # 処理後の時刻
        # t2 = time.time()

        # # 経過時間を表示
        # elapsed_time = t2-t1
        # print(f"経過時間:{elapsed_time}")

        if results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, results.multi_hand_landmarks[0], mp_holistic.HAND_CONNECTIONS)
        video.write(image)

        cv2.imshow('MediaPipe Hand', image)
        if cv2.waitKey(20) & 0xFF == 27:
            break
cap.release()
video.release()
