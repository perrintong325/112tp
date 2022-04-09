from cmu_cs3_graphics import *
from PIL import Image
import cv2
import mediapipe as mp

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands.Hands()
vid = cv2.VideoCapture(1)

def onAppStart(app):
    app.vid = vid
    app.hasFrame = False

def redrawAll(app):
    if app.hasFrame:
        image = cv2.flip(cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB),1)
        results = hands.process(image)
        if results.multi_hand_landmarks:
            for landmark in results.multi_hand_landmarks:
                drawing.draw_landmarks(image,landmark,mp.solutions.hands.HAND_CONNECTIONS) 
            drawPILImage(Image.fromarray(image), 0, 0)
            for landmark in results.multi_hand_landmarks:
                drawing.draw_landmarks(image,landmark,mp.solutions.hands.HAND_CONNECTIONS)
                for num,pos in enumerate(landmark.landmark):
                    y,x,colour = image.shape
                    # !!!won't run without int!!! keep it
                    cx = int(pos.x * x)
                    cy = int(pos.y*y)
                    # cv2.circle(rgbImage, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                    drawCircle(cx,cy,15,fill='green')
        else:
            drawPILImage(Image.fromarray(app.frame), 0, 0)
                
        

def onStep(app):
    status, app.frame = app.vid.read()
    app.hasFrame = True

def main():
    _,image = vid.read()
    y,x,c = image.shape
    runApp(width=x,height=y)
    

main()



# #reference: google mediaPipe docs
# while True:
#     status, image = vid.read()
#     image = cv2.flip(image,1)
#     results = hands.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
#     if results.multi_hand_landmarks:
#         for landmark in results.multi_hand_landmarks:
#             for num,pos in enumerate(landmark.landmark):
#                 y,x,colour = image.shape
#                 # !!!won't run without int!!! keep it
#                 cx = int(pos.x * x)
#                 cy = int(pos.y*y)
#                 cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
#             drawing.draw_landmarks(image,landmark,mp.solutions.hands.HAND_CONNECTIONS)
#     cv2.imshow("image",image)
#     cv2.waitKey(1)

