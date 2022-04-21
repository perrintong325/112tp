from cmu_cs3_graphics import *
from PIL import Image
import cv2
import mediapipe as mp
import math
import random

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
camNum = -1
for cam in range(2):
    vid = cv2.VideoCapture(cam)
    if vid.isOpened():
        camNum = cam
if camNum == -1:
    print("No camera detected")
    quit()
vid = cv2.VideoCapture(camNum)

# reference: Google MediaPipe doc
class handDetector(object):
    def __init__(self, maxHands, minDetectionConf, minTrackConf):
        self.maxHands = maxHands
        self.minDetectionConf = minDetectionConf
        self.minTrackConf = minTrackConf

    def drawDots(self, image):
        if self.results.multi_hand_landmarks:
            for landmark in self.results.multi_hand_landmarks:
                for pos in landmark.landmark:
                    y, x, colour = image.shape
                    # !!!won't run without int!!! keep it
                    cx = pos.x * x
                    cy = pos.y*y
                    drawCircle(cx, cy, 15, fill='green')
                    #cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    def findHands(self, image):
        self.results = mp_hands.Hands(max_num_hands=self.maxHands,
                                      min_detection_confidence=self.minDetectionConf,
                                      min_tracking_confidence=self.minTrackConf).process(image)
        if self.results.multi_hand_landmarks:
            for landmark in self.results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    image, landmark, mp_hands.HAND_CONNECTIONS)
        return image


mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection


class headDetector(object):
    def __init__(self, minDetectionConf):
        self.minDetectionConf = minDetectionConf

    def findHeads(self, image,app):
        self.results = mp_face_detection.FaceDetection(
            min_detection_confidence=self.minDetectionConf).process(image)
        if self.results.detections:
            for head in self.results.detections:
                mp_draw.draw_detection(image, head)
            for noses in self.results.detections:
                location = mp_face_detection.get_key_point(noses, mp_face_detection.FaceKeyPoint.NOSE_TIP)
                cx = location.x * app.width
                cy = location.y * app.height
                app.noses.append((cx, cy))
        return image
    

class Bomb(object):
    def __init__(self,app):
        self.cx = random.choice([0, app.width])
        self.cy = random.randrange(0, app.height)
        # self.cy = 1080
        self.xVelocity = app.width/20
        self.yVelocity = -5
        self.xAcceleration = 0
        self.yAcceleration = 9.8
        self.r = 10
        self.color = 'red'

def pathFinding(x0,y0,xMax,yMax,xVelocity,xAcceleration,yAcceleration):
# def pathFinding(x0,xMax,xVelocity,xAcceleration,yAcceleration):
    # if y0<=yMax:
    #     return 500
    # else:
    #     # theta = math.atan((y0-yMax)/(x0-xMax))
    #     # velocity = math.sqrt((y0-yMax)*2/(math.sin(theta)**2))
    #     # return (math.sqrt((velocity**2)-(xVelocity**2)))
    #     print('test')
    #     return (yMax-y0)*((xMax-x0)/xVelocity)
    t = (xMax-x0)/xVelocity
    if y0<=yMax:
        return ((yMax-y0)/t)-(0.5*yAcceleration*t)
    else:
        return ((yMax-y0)-(0.5*yAcceleration*(t**2)))/t


class SmartBomb(Bomb):
    def __init__(self,app,targetX,targetY):
        super().__init__(app)
        # self.yVelocity = pathFinding(self.cx,self.cy,targetX,targetY,self.xVelocity)
        self.yVelocity = pathFinding(self.cx,self.cy,targetX,targetY,self.xVelocity,self.xAcceleration,self.yAcceleration)
        #self.yVelocity = pathFinding(self.cx,self.cy,app.width/2,app.height/2,self.xVelocity,self.xAcceleration,self.yAcceleration)

#def onAppStart(app):
def handModeOnAppStart(app):
    app.vid = vid
    app.hasFrame = False
    app.stepsPerSecond = 30
    app.bombs = []
    app.noses = list()


#def redrawAll(app):
def handModeRedrawAll(app):
    if app.hasFrame:
        image = cv2.flip(cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB), 1)
        image = app.handDetector.findHands(image)
        image = app.headDetector.findHeads(image,app)
        drawImage(CMUImage(Image.fromarray(image)), 0, 0)
        app.handDetector.drawDots(image)
    for bomb in app.bombs:
        drawCircle(bomb.cx, bomb.cy, bomb.r, fill=bomb.color)


#def onStep(app):
def handModeOnStep(app):
    app.handDetector = handDetector(4, 0.3, 0.3)
    app.headDetector = headDetector(0.3)
    status, app.frame = app.vid.read()
    app.hasFrame = True
    if app.noses!=[]:
        app.bombs.append(SmartBomb(app,app.noses[0][0],app.noses[0][1]))
        app.noses.pop(0)
    for bomb in app.bombs:
        bomb.cx += bomb.xVelocity
        bomb.cy += bomb.yVelocity
        bomb.xVelocity += bomb.xAcceleration
        bomb.yVelocity += bomb.yAcceleration
    removeable = []
    for bomb in app.bombs:
        if bomb.cx > app.width or bomb.cx < 0:
            removeable.append(bomb)
        if bomb.cy > app.height or bomb.cy < 0:
            removeable.append(bomb)
    for bomb in set(removeable):
        app.bombs.remove(bomb)


def main():
    _, image = vid.read()
    y, x, c = image.shape
    print(x,y)
    runApp(width=x, height=y)


if __name__ == '__main__':
    main()
