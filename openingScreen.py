from cmu_cs3_graphics import *
from PIL import Image

#this file displays the opebing screen/menu of the game.

def onAppStart(app):
    #source: self screenshot from Fruit Ninja iPad game + Photoshop
    app.backgroundImage = CMUImage(Image.open('Resources/background.png'))
    #source: https://logos.fandom.com/wiki/Fruit_Ninja + Photoshop
    app.logo = CMUImage(Image.open('Resources/FruitNinja.png'))
    #source: Photoshop self made
    app.normalModeImage = Image.open('Resources/normalMode.png').convert('RGBA')
    #source: Photoshop self made
    app.handModeImage = Image.open('Resources/handMode.png')
    app.handModeX, app.handModeY = 5*app.width//8, 3*app.height//8
    app.normalModeX, app.normalModeY = app.width//8, 3*app.height//8
    app.normalModeWidth, app.normalModeHeight = app.normalModeImage.width, app.normalModeImage.height
    app.handModeWidth, app.handModeHeight = app.handModeImage.width, app.handModeImage.height
    app.normalModeImage = CMUImage(app.normalModeImage)
    app.handModeImage = CMUImage(app.handModeImage)
    app.status = 'splashScreen'
    app.splashScreenLeave = False

def onStep(app):
    if app.splashScreenLeave!=False:
        app.normalModeX -= 30
        app.handModeX += 30
        if app.normalModeX <= 0 and app.handModeX >= app.width:
            app.status = app.splashScreenLeave
            app.handModeX, app.handModeY = 5*app.width//8, 3*app.height//8
            app.normalModeX, app.normalModeY = app.width//8, 3*app.height//8
            app.splashScreenLeave = False

def onMousePress(app,mouseX,mouseY):
    if (mouseX >= app.handModeX and mouseX <= app.handModeX + app.handModeWidth and \
    mouseY >= app.handModeY and mouseY <= app.handModeY + app.handModeHeight):
        app.splashScreenLeave = 'hand'
    elif (mouseX >= app.normalModeX and mouseX <= app.normalModeX + app.normalModeWidth and
    mouseY >= app.normalModeY and mouseY <= app.normalModeY + app.normalModeHeight):
        app.splashScreenLeave = 'normal'

def redrawAll(app):
    drawImage(app.backgroundImage, 0, 0)
    drawImage(app.logo, 0, 0,width=1.6*(app.width/8),height=app.width/8)
    drawImage(app.normalModeImage, app.normalModeX, app.normalModeY, width=app.width//4, height=app.width//4)
    drawImage(app.handModeImage, app.handModeX, app.handModeY, width=app.width//4, height=app.width//4)


if __name__ == '__main__':
    runApp(width=1280, height=720)


