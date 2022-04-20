from cmu_cs3_graphics import *
from PIL import Image

import openingScreen
import fruitMovement

def onAppStart(app):
    openingScreen.openingScreenOnAppStart(app)
    fruitMovement.fruitMovementOnAppStart(app)
    app.stepsPerSecond = 120

def onStep(app):
    if app.status == 'splashScreen':
        openingScreen.openingScreenOnStep(app)
    if app.status == 'normal':
        fruitMovement.fruitMovementOnStep(app)

def onMousePress(app,mouseX,mouseY):
    if app.status == 'splashScreen':
        openingScreen.openingScreenOnMousePress(app,mouseX,mouseY)

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

runApp(width=1920, height=1080)