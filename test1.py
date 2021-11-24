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

background_list = []
for file_name in file_list:
    root, ext = os.path.splitext(file_name)
    if ext == u'.png' or u'.jpeg' or u'.jpg':
        abs_name = data_dir_path + '/' + file_name
        image = cv2.imread(abs_name)
        background_list.append(Background(image))


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
            print(image.shape)
            for background in background_list:
                background.resize_per(high, wide, obj_per)
                print(background.img.shape)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_list = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                hand = Hand(hand_landmarks.landmark, wide, high)
                hand_list.append(hand)

        near_index = []
        if hand_list != []:
            for i, background in enumerate(background_list):
                near_index.append(0)
                for j, hand in enumerate(hand_list):
                    if j == 0:
                        continue

                    im_center_x, im_center_y = background.center()
                    print("im_point", background.point_x, background.point_y)
                    print("im_center", im_center_x, im_center_y)
                    if comp_point(im_center_x, im_center_y, hand.centerx, hand.centery, hand_list[near_index[i]].centerx, hand_list[near_index[i]].centery) == 1:
                        near_index[i] = j

            # 画像を動かしたりする処理
            cnt = 0
            for background in background_list:
                if cnt != 0:
                    cnt -= 1
                    continue

                if near_index == []:
                    break

                now_index = near_index[0]
                if background.ispointin(hand_list[now_index].centerx, hand_list[now_index].centery) is True:
                    if hand_list[now_index].ishand_close() is True and background.move_flag is False:
                        background.set_abspoint(
                            hand_list[now_index].centerx, hand_list[now_index].centery)

                    if background.move_flag is True and hand_list[now_index].ishand_open() is True:
                        background.fin_change()

                if background.move_flag is True:
                    background.change_point(
                        hand_list[now_index].centerx, hand_list[now_index].centery, wide, high)
                    # 一つの手に2つ以上の画像を持たせないようにする処理
                    # near_index = [
                    #     index for index in near_index if index != now_index]
                    for j in near_index:
                        if j == now_index:
                            near_index.remove(j)
                            cnt += 1

        fit_imlist = []
        for i, background in enumerate(background_list):
            if background.move_flag is True:
                fit_imlist.insert(len(fit_imlist), background)
            else:
                fit_imlist.insert(0, background)

        for background in fit_imlist:
            if background.move_flag is True:
                background.del_frame()
                background.add_frame(5, [0, 0, 255])
                background.comb_main(image)
            else:
                background.del_frame()
                background.add_frame(5, [0, 255, 0])
                background.comb_main(image)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
