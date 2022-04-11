from cmu_cs3_graphics import *
import random

x,y = 400, 400
#temporary test class
class Fruit(object):
    def __init__(self):
        self.cx = random.randint(0,x)
        self.cy = y
        self.xVelocity = random.randint(-30,30)
        self.yVelocity = random.randint(-75,-10)


def onAppStart(app):
    app.fruits = [Fruit()]
    # app.stepsPerSecond = 30
    app.count = 0

def onStep(app):
    app.count+=1
    if app.count%10 == 0:
        app.fruits.append(Fruit())

def redrawAll(app):
    removeable = []
    for fruit in app.fruits:
        print(fruit.cx,fruit.cy)
        if fruit.cx >x or fruit.cx <0 or fruit.cy > y or fruit.cy<0:
            removeable.append(fruit)
        else:
            fruit.cx += fruit.xVelocity
            fruit.cy += fruit.yVelocity
            fruit.yVelocity += 5
            drawCircle(fruit.cx,fruit.cy,10,fill='red')
    # for fruit in removeable:
    #     app.fruit.remove(fruit)

runApp(width=x,height=y)