from cmu_cs3_graphics import *
from PIL import Image

# def onAppStart(app):
def openingScreenOnAppStart(app):
    app.backgroundImage = Image.open('background.png')
    app.logo = Image.open('FruitNinja.png')
    app.normalModeImage = Image.open('normalMode.png')
    app.handModeImage = Image.open('handMode.png')
    app.handModeX, app.handModeY = 5*app.width//8, 3*app.height//8
    app.normalModeX, app.normalModeY = app.width//8, 3*app.height//8
    app.status = 'splashScreen'
    app.splashScreenLeave = False

# def onStep(app):
def openingScreenOnStep(app):
    if app.splashScreenLeave:
        app.normalModeX -= 30
        app.handModeX += 30
        if app.normalModeX <= 0 and app.handModeX >= app.width:
            app.status = 'normal'
            app.handModeX, app.handModeY = 5*app.width//8, 3*app.height//8
            app.normalModeX, app.normalModeY = app.width//8, 3*app.height//8
            app.splashScreenLeave = False

# def onMousePress(app,mouseX,mouseY):
def openingScreenOnMousePress(app,mouseX,mouseY):
    if (mouseX >= app.handModeX and mouseX <= app.handModeX + app.handModeImage.width and \
    mouseY >= app.handModeY and mouseY <= app.handModeY + app.handModeImage.height):
        app.status = 'hand'
    elif (mouseX >= app.normalModeX and mouseX <= app.normalModeX + app.normalModeImage.width and
    mouseY >= app.normalModeY and mouseY <= app.normalModeY + app.normalModeImage.height):
        app.splashScreenLeave = True

# def redrawAll(app):
def openingScreenRedrawAll(app):
    drawImage(CMUImage(app.backgroundImage), 0, 0)
    drawImage(CMUImage(app.logo), 0, 0,width=1.6*(app.width/6),height=app.width/6)
    drawImage(CMUImage(app.normalModeImage), app.normalModeX, app.normalModeY)
    drawImage(CMUImage(app.handModeImage), app.handModeX, app.handModeY)


if __name__ == '__main__':
    runApp(width=1920, height=1080)


