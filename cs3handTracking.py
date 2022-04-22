from cmu_cs3_graphics import *
from PIL import Image
import cv2
import mediapipe as mp
import math
import random
import fruitMovement

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

# reference: https://google.github.io/mediapipe/solutions/hands.html
class handDetector(object):
    def __init__(self, maxHands, minDetectionConf, minTrackConf):
        self.maxHands = maxHands
        self.minDetectionConf = minDetectionConf
        self.minTrackConf = minTrackConf

    def drawDots(self, image,app):
        if self.results.multi_hand_landmarks:
            for landmark in self.results.multi_hand_landmarks:
                for pos in landmark.landmark:
                    y, x, _ = image.shape
                    # !!!won't run without int!!! keep it
                    cx = pos.x * x
                    cy = pos.y*y
                    app.handPoints.append((cx,cy))
                    # drawCircle(cx, cy, 15, fill='green')

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

#reference: https://google.github.io/mediapipe/solutions/face_detection.html
class headDetector(object):
    results = None
    def __init__(self, minDetectionConf):
        self.minDetectionConf = minDetectionConf

    def findHeads(self, image,app):
        headDetector.results = mp_face_detection.FaceDetection(
            min_detection_confidence=self.minDetectionConf).process(image)
        if headDetector.results.detections:
            for head in headDetector.results.detections:
                mp_draw.draw_detection(image, head)
            for noses in headDetector.results.detections:
                location = mp_face_detection.get_key_point(noses, mp_face_detection.FaceKeyPoint.NOSE_TIP)
                cx = location.x * app.width
                cy = location.y * app.height
                app.noses.append((cx, cy))
        return image
    
    def boxLocation(self,app):
        if headDetector.results.detections:
            #reference: https://stackoverflow.com/questions/69810210/mediapipe-solutionfacedetection
            for head in headDetector.results.detections:
                location = head.location_data
                app.headBoxXmin = location.relative_bounding_box.xmin*app.width
                app.headBoxYmin = location.relative_bounding_box.ymin*app.height
                app.headBoxWidth = location.relative_bounding_box.width*app.width
                app.headBoxHeight = location.relative_bounding_box.height*app.height

class Bomb(object):
    def __init__(self,app):
        self.cx = random.choice([0, app.width])
        self.cy = random.randrange(0, app.height)
        self.xVelocity = app.width/20
        self.yVelocity = -5
        self.xAcceleration = 0
        self.yAcceleration = 9.8
        self.r = 10
        self.color = 'red'
        self.points = 10

def pathFinding(x0,y0,xMax,yMax,xVelocity,xAcceleration,yAcceleration):
    t = (xMax-x0)/xVelocity
    if y0<=yMax:
        return ((yMax-y0)/t)-(0.5*yAcceleration*t)
    else:
        return ((yMax-y0)-(0.5*yAcceleration*(t**2)))/t


class SmartBomb(Bomb):
    def __init__(self,app,targetX,targetY):
        super().__init__(app)
        self.yVelocity = pathFinding(self.cx,self.cy,targetX,targetY,self.xVelocity,self.xAcceleration,self.yAcceleration)
        self.color = 'green'

def onAppStart(app):
    app.vid = vid
    app.hasFrame = False
    app.stepsPerSecond = 60
    app.smartBombs = []
    app.noses = []
    app.handPoints = []
    app.headBoxXmin = None
    app.headBoxYmin = None
    app.headBoxWidth = None
    app.headBoxHeight = None


def redrawAll(app):
    if app.hasFrame:
        image = cv2.flip(cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB), 1)
        image = cv2.resize(image, (app.width, app.height))
        image = app.handDetector.findHands(image)
        image = app.headDetector.findHeads(image,app)
        drawImage(CMUImage(Image.fromarray(image)), 0, 0)
        app.handDetector.drawDots(image,app)
    for bomb in app.smartBombs:
        drawCircle(bomb.cx, bomb.cy, bomb.r, fill=bomb.color)


def onStep(app):
    for p in app.handPoints:
        fruitMovement.onMouseMove(app,p[0],p[1])
    if app.count % 10 == 0:
        app.movement = []
        app.handPoints = []
    app.handDetector = handDetector(4, 0.3, 0.3)
    app.headDetector = headDetector(0.3)
    _, app.frame = app.vid.read()
    app.hasFrame = True
    if app.noses!=[]:
        app.headDetector.boxLocation(app)
        app.smartBombs.append(SmartBomb(app,app.noses[0][0],app.noses[0][1]))
        app.noses.pop(0)
    for bomb in app.smartBombs:
        bomb.cx += bomb.xVelocity
        bomb.cy += bomb.yVelocity
        bomb.xVelocity += bomb.xAcceleration
        bomb.yVelocity += bomb.yAcceleration
    removeable = []
    for bomb in app.smartBombs:
        if bomb.cy >app.headBoxYmin and bomb.cy < app.headBoxYmin+app.headBoxHeight and bomb.cx > app.headBoxXmin and bomb.cx < app.headBoxXmin+app.headBoxWidth:
            app.points -= bomb.points
        elif bomb.cx > app.width or bomb.cx < 0:
            removeable.append(bomb)
        elif bomb.cy > app.height or bomb.cy < 0:
            removeable.append(bomb)
        
    for bomb in set(removeable):
        app.smartBombs.remove(bomb)


def main():
    runApp(width=1280, height=720)


if __name__ == '__main__':
    main()
