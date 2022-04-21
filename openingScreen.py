from cmu_cs3_graphics import *
from PIL import Image

def onAppStart(app):
    app.backgroundImage = Image.open('Resources/background.png')
    app.logo = Image.open('Resources/FruitNinja.png')
    app.normalModeImage = Image.open('Resources/normalMode.png').convert('RGBA')
    app.handModeImage = Image.open('Resources/handMode.png')
    app.handModeX, app.handModeY = 5*app.width//8, 3*app.height//8
    app.normalModeX, app.normalModeY = app.width//8, 3*app.height//8
    app.status = 'splashScreen'
    app.splashScreenLeave = False

def onStep(app):
    if app.splashScreenLeave!=False:
        app.normalModeX -= 50
        app.handModeX += 50
        if app.normalModeX <= 0 and app.handModeX >= app.width:
            app.status = app.splashScreenLeave
            app.handModeX, app.handModeY = 5*app.width//8, 3*app.height//8
            app.normalModeX, app.normalModeY = app.width//8, 3*app.height//8
            app.splashScreenLeave = False

def onMousePress(app,mouseX,mouseY):
    if (mouseX >= app.handModeX and mouseX <= app.handModeX + app.handModeImage.width and \
    mouseY >= app.handModeY and mouseY <= app.handModeY + app.handModeImage.height):
        app.splashScreenLeave = 'hand'
    elif (mouseX >= app.normalModeX and mouseX <= app.normalModeX + app.normalModeImage.width and
    mouseY >= app.normalModeY and mouseY <= app.normalModeY + app.normalModeImage.height):
        app.splashScreenLeave = 'normal'

def redrawAll(app):
    drawImage(CMUImage(app.backgroundImage), 0, 0)
    drawImage(CMUImage(app.logo), 0, 0,width=1.6*(app.width/8),height=app.width/8)
    drawImage(CMUImage(app.normalModeImage), app.normalModeX, app.normalModeY, width=app.width//4, height=app.width//4)
    drawImage(CMUImage(app.handModeImage), app.handModeX, app.handModeY, width=app.width//4, height=app.width//4)


if __name__ == '__main__':
    runApp(width=1280, height=720)


