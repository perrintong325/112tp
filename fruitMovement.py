from cmu_cs3_graphics import *
import random
import math

x,y = 400, 400
#temporary test class
class Fruit(object):
    def __init__(self):
        self.cx = random.randrange(0,x)
        self.cy = y
        self.xVelocity = random.randrange(-30,30)
        self.yVelocity = random.randint(-y//8,-y//22)
        self.r = random.randrange(5,15)

def onAppStart(app):
    app.fruits = [Fruit()]
    # app.stepsPerSecond = 30
    app.count = 0

#reference: cs academy
def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def onMousePress(app,mouseX,mouseY):
    for fruit in app.fruits:
        if distance(mouseX,mouseY,fruit.cx,fruit.cy)<= fruit.r:
            #how to decide wt shape?
            
            pass

def onStep(app):
    app.count+=1
    if app.count%10 == 0:
        app.fruits.append(Fruit())
    removeable = []
    for fruit in app.fruits:
        if fruit.cx >x or fruit.cx <0 or fruit.cy > y or fruit.cy<0:
            removeable.append(fruit)
    for fruit in removeable:
        app.fruits.remove(fruit)

def redrawAll(app):
    for fruit in app.fruits:
        fruit.cx += fruit.xVelocity
        fruit.cy += fruit.yVelocity
        fruit.yVelocity += 5
        drawCircle(fruit.cx,fruit.cy,fruit.r,fill='red')

runApp(width=x,height=y)