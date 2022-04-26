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
    openingScreen.onAppStart(app)
    fruitMovement.onAppStart(app)
    handMode.onAppStart(app)
    app.backButtonImage = Image.open('Resources/backButton.png')
    app.backButtonWidth, app.backButtonHeight = app.backButtonImage.width, app.backButtonImage.height
    app.backButtonImage = CMUImage(app.backButtonImage.resize((app.width//10,app.width//10)))
    app.stepsPerSecond = 30

def onStep(app):
    if app.status == 'splashScreen':
        openingScreen.onStep(app)
    elif app.status == 'normal':
        fruitMovement.onStep(app)
    elif app.status == 'hand':
        handMode.onStep(app)
        fruitMovement.onStep(app)

def onMousePress(app,mouseX,mouseY):
    if app.status == 'splashScreen':
        openingScreen.onMousePress(app,mouseX,mouseY)
    elif app.status == 'normal' or app.status == 'hand':
        if mouseX >= 0 and mouseX <= app.backButtonWidth and \
        mouseY >= app.height-app.backButtonHeight-10 and mouseY <= app.height-10:
            app.status = 'splashScreen'
            app.splashScreenLeave = False
            fruitMovement.onAppStart(app)
            handMode.onAppStart(app)

def onMouseMove(app,mouseX,mouseY):
    if app.status == 'normal':
        fruitMovement.onMouseMove(app,mouseX,mouseY)

def redrawAll(app):
    if app.status == 'splashScreen':
        openingScreen.redrawAll(app)
    elif app.status == 'normal':
        drawImage(app.backgroundImage, 0, 0)
        drawImage(app.logo, 0, 0,width=1.6*(app.width/8),height=app.width/8)
        fruitMovement.redrawAll(app)
        drawImage(app.backButtonImage, 0, app.height-app.backButtonHeight-10)
    elif app.status == 'hand':
        handMode.redrawAll(app)
        drawImage(app.logo, 0, 0,width=1.6*(app.width/8),height=app.width/8)
        drawImage(app.backButtonImage, 0, app.height-app.backButtonHeight-10)
        fruitMovement.redrawAll(app)
        

runApp(width=1280, height=720)