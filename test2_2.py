import os

import mediapipe as mp
import cv2

from hand_class import Hand
from hand_class import comp_point
from background_class import Background


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.hands

obj_per = 2
data_dir_path = u"./img/"
file_list = os.listdir(r'./img/')

img_list = []
for file_name in file_list:
    root, ext = os.path.splitext(file_name)
    if ext == u'.png' or u'.jpeg' or u'.jpg':
        abs_name = data_dir_path + '/' + file_name
        image = cv2.imread(abs_name)
        img_list.append(Background(image))


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

        wide = image.shape[1]
        high = image.shape[0]

        if first_loop is True:
            first_loop = False
            for img in img_list:
                img.resize_per(high, wide, obj_per)
                print(img.img.shape)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_list = []
        if results.multi_hand_landmarks:
            hand_cnt = 0
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                hand = Hand(hand_landmarks.landmark, wide, high)
                hand_list.append(hand)

        near_index = []
        if hand_list != []:
            for i, img in enumerate(img_list):
                near_index.append(0)
                for j, hand in enumerate(hand_list):
                    if j == 0:
                        continue

                    im_center_x, im_center_y = img.center()
                    if comp_point(im_center_x, im_center_y, hand.centerx, hand.centery, hand_list[near_index[i]].centerx, hand_list[near_index[i]].centery) == 1:
                        near_index[i] = j

            for i, img in enumerate(img_list):

                if img.ispointin(hand_list[near_index[i]].centerx, hand_list[near_index[i]].centery) is True:
                    if hand_list[near_index[i]].ishand_close() is True and img.move_flag is False:
                        img.set_abspoint(
                            hand_list[near_index[i]].centerx, hand_list[near_index[i]].centery)

                    if img.move_flag is True and hand_list[near_index[i]].ishand_open() is True:
                        img.fin_change()

                if img.move_flag is True and hand_cnt == 0:
                    img.change_point(
                        hand_list[near_index[i]].centerx, hand_list[near_index[i]].centery, wide, high)

        for img in img_list:
            if img.move_flag is True:
                img.del_frame()
                img.add_frame(5, [0, 0, 255])
                image[img.point_y:img.point_y+img.img.shape[0],
                      img.point_x:img.point_x+img.img.shape[1]] = img.img
            else:
                img.del_frame()
                img.add_frame(5, [0, 255, 0])
                image[img.point_y:img.point_y+img.img.shape[0],
                      img.point_x:img.point_x+img.img.shape[1]] = img.img

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
