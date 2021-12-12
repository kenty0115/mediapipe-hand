import mediapipe as mp
import cv2

from hand_class import Hand
from backgrounds_class import Backgrounds
from comb_imghand import Imhand


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.hands

obj_per = 3
img_path = "./img/"

first_loop = True
cv2.namedWindow('MediaPipe Hand', cv2.WINDOW_AUTOSIZE)
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
            hand_landmarks = results.multi_hand_landmarks[0]
            hand_class = Hand(
                results.multi_hand_landmarks[0].landmark, heigh, width)
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        if hand_class != None:

            imhand = Imhand(backgrounds_class.background_list, hand_class)
            imhand.background_adhand()

            imhand.set_moveflag()
            imhand.change_background_point()

        backgrounds_class.set_fitlist()

        image = backgrounds_class.fit_main(image)

        cv2.imshow('MediaPipe Hand', image)
        if cv2.waitKey(20) & 0xFF == 27:
            break
cap.release()
