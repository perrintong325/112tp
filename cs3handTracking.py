from cmu_cs3_graphics import *
from PIL import Image
import cv2
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
vid = cv2.VideoCapture(1)

#reference: Google MediaPipe doc
class handDetector(object):
    def __init__(self,maxHands,minDetectionConf,minTrackConf):
        self.maxHands = maxHands
        self.minDetectionConf = minDetectionConf
        self.minTrackConf = minTrackConf

    def drawDots(self,image):
        if self.results.multi_hand_landmarks:
            for landmark in self.results.multi_hand_landmarks:
                for pos in landmark.landmark:
                        y,x,colour = image.shape
                        # !!!won't run without int!!! keep it
                        cx = pos.x * x
                        cy = pos.y*y
                        drawCircle(cx,cy,15,fill='green')
                        #cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    
    def findHands(self,image):
        self.results = mp_hands.Hands(max_num_hands = self.maxHands,
                    min_detection_confidence=self.minDetectionConf,
                    min_tracking_confidence=self.minTrackConf).process(image)
        if self.results.multi_hand_landmarks:
            for landmark in self.results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image,landmark,mp_hands.HAND_CONNECTIONS)
        return image

mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection

class headDetector(object):
    def __init__(self,minDetectionConf):
        self.minDetectionConf = minDetectionConf
    
    def findHeads(self,image):
        self.results = mp_face_detection.FaceDetection(min_detection_confidence=self.minDetectionConf).process(image)
        if self.results.detections:
            for head in self.results.detections:
                mp_draw.draw_detection(image,head)
        return image

def onAppStart(app):
    app.vid = vid
    app.hasFrame = False
    app.handMode = 1
    app.stepsPerSecond = 600

def redrawAll(app):
    if app.hasFrame:
        image = cv2.flip(cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB),1)
        if app.handMode == 1:
            image = app.handDetector.findHands(image)
            drawPILImage(Image.fromarray(image), 0, 0)
            # cv2.imshow("image",image)
            app.handDetector.drawDots(image)
        else:
            image = app.headDetector.findHeads(image)
            drawPILImage(Image.fromarray(image), 0, 0)
    drawLabel(f"Hand Mode = {bool(app.handMode)}",100,100,size = 30,
                fill='lawnGreen', align='left')

def onKeyPress(app,key):
    if key == 'space':
        app.handMode -= 1
        app.handMode = abs(app.handMode)

def onStep(app):
    app.handDetector = handDetector(4,0.3,0.3)
    app.headDetector = headDetector(0.3)
    status, app.frame = app.vid.read()
    app.hasFrame = True

def main():
    _,image = vid.read()
    y,x,c = image.shape
    runApp(width=x,height=y)

main()