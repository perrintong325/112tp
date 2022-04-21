from cmu_cs3_graphics import *
from PIL import Image
import cv2

import openingScreen
import fruitMovement
import cs3handTracking as handMode

camNum = -1
for cam in range(2):
    vid = cv2.VideoCapture(cam)
    if vid.isOpened():
        camNum = cam
if camNum == -1:
    print("No camera detected")
    quit()
vid = cv2.VideoCapture(camNum)

def onAppStart(app):
    openingScreen.openingScreenOnAppStart(app)
    fruitMovement.fruitMovementOnAppStart(app)
    handMode.handModeOnAppStart(app)
    app.backButtonImage = Image.open('Resources/backButton.png')
    app.stepsPerSecond = 30

def onStep(app):
    if app.status == 'splashScreen':
        openingScreen.openingScreenOnStep(app)
    elif app.status == 'normal':
        fruitMovement.fruitMovementOnStep(app)
    elif app.status == 'hand':
        handMode.handModeOnStep(app)
        fruitMovement.fruitMovementOnStep(app)

def onMousePress(app,mouseX,mouseY):
    if app.status == 'splashScreen':
        openingScreen.openingScreenOnMousePress(app,mouseX,mouseY)
    elif app.status == 'normal' or app.status == 'hand':
        if mouseX >= 0 and mouseX <= app.backButtonImage.width and \
        mouseY >= app.height-250 and mouseY <= app.height-250+app.backButtonImage.height:
            app.status = 'splashScreen'
            app.splashScreenLeave = False
            fruitMovement.fruitMovementOnAppStart(app)
            handMode.handModeOnAppStart(app)

def onMouseMove(app,mouseX,mouseY):
    if app.status == 'normal':
        fruitMovement.fruitMovementOnMouseMove(app,mouseX,mouseY)

def redrawAll(app):
    if app.status == 'splashScreen':
        openingScreen.openingScreenRedrawAll(app)
    elif app.status == 'normal':
        drawImage(CMUImage(app.backgroundImage), 0, 0)
        drawImage(CMUImage(app.logo), 0, 0,width=1.6*(app.width/6),height=app.width/6)
        fruitMovement.fruitMovementRedrawAll(app)
        drawImage(CMUImage(app.backButtonImage), 0, app.height-250)
    elif app.status == 'hand':
        handMode.handModeRedrawAll(app)
        drawImage(CMUImage(app.logo), 0, 0,width=1.6*(app.width/6),height=app.width/6)
        drawImage(CMUImage(app.backButtonImage), 0, app.height-250)
        fruitMovement.fruitMovementRedrawAll(app)

runApp(width=1920, height=1080)