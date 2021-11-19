import mediapipe as mp
import cv2

from hand_class import Hand
from background_class import Background


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.hands

obj_per = 2
img_path = "img/"
obj_img = cv2.imread(img_path + "background.jpg")

obj_class = Background(obj_img)


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
            obj_class.resize_per(high, wide, obj_per)
            print(obj_class.img.shape)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            hand_cnt = 0
            for j, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                hand = Hand(hand_landmarks.landmark, wide, high)
                try:
                    if obj_class.ispointin(hand.centerx, hand.centery) is True:
                        if hand.ishand_close() is True and obj_class.move_flag is False:
                            obj_class.set_abspoint(hand.centerx, hand.centery)

                        if obj_class.move_flag is True and hand.ishand_open() is True:
                            obj_class.fin_change()

                    if obj_class.move_flag is True and hand_cnt == 0:
                        hand_cnt += 1
                        obj_class.change_point(
                            hand.centerx, hand.centery, wide, high)

                except Exception:
                    pass

        if obj_class.move_flag is True:
            obj_class.del_frame()
            obj_class.add_frame(5, [0, 0, 255])
            image[obj_class.img_pointy:obj_class.img_pointy+obj_class.img.shape[0],
                  obj_class.img_pointx:obj_class.img_pointx+obj_class.img.shape[1]] = obj_class.img
        else:
            obj_class.del_frame()
            obj_class.add_frame(5, [0, 255, 0])
            image[obj_class.img_pointy:obj_class.img_pointy+obj_class.img.shape[0],
                  obj_class.img_pointx:obj_class.img_pointx+obj_class.img.shape[1]] = obj_class.img

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
