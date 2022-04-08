import cv2 
import mediapipe as mp

vid = cv2.VideoCapture(1)
drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands.Hands()

#reference: google mediaPipe docs
while True:
    status, image = vid.read()
    image = cv2.flip(image,1)
    results = hands.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for landmark in results.multi_hand_landmarks:
            for num,pos in enumerate(landmark.landmark):
                y,x,colour = image.shape
                # !!!won't run without int!!! keep it
                cx = int(pos.x * x)
                cy = int(pos.y*y)
                cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            drawing.draw_landmarks(image,landmark,mp.solutions.hands.HAND_CONNECTIONS)
    cv2.imshow("image",image)
    cv2.waitKey(1)

