from cmu_cs3_graphics import *
import random
import math

x,y = 400, 400
#temporary test class
class Fruit(object):
    def __init__(self):
        self.cx = random.randrange(0,x)
        self.cy = y/2
        self.xVelocity = random.randrange(-1,1)
        self.yVelocity = random.randint(-y//50,-y//70)
        # self.r = random.randrange(5,15)
        self.r = 20

def onAppStart(app):
    app.fruits = [Fruit()]
    app.count = 0
    # app.removeable = []
    app.handX = -1
    app.handY = -1
    app.stepsPerSecond = 5
    app.movement = []
    app.moveCount = 0

#reference: cs academy
def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# def onMouseMove(app,mouseX,mouseY):
#     app.handX = mouseX
#     app.handY = mouseY
#     # for fruit in app.fruits:
#     #     if distance(mouseX,mouseY,fruit.cx,fruit.cy)<= fruit.r:
#     #         #how to decide wt shape?
#     #         # app.removable.append(fruit)
#     #         print(fruit)
#     #         app.fruits.remove(fruit)

def onMouseDrag(app,mouseX,mouseY):
    app.handX = mouseX
    app.handY = mouseY
    app.movement.append((mouseX,mouseY))
    

def onStep(app):
    app.count+=1
    app.moveCount += 1
    if app.moveCount > len(app.movement)+10:
        app.movement = []
    if app.count%10 == 0:
        app.fruits.append(Fruit())
    removeable = []
    for fruit in app.fruits:
        if fruit.cx >x or fruit.cx <0 or fruit.cy > y or fruit.cy<0:
            # app.removeable.append(fruit)
            removeable.append(fruit)
        # elif distance(app.handX,app.handY,fruit.cx,fruit.cy)<= fruit.r+10:
        #     removeable.append(fruit)
        else:
            for l in range(1,len(app.movement)):
                if (distance(app.movement[l-1][0],app.movement[l-1][1],fruit.cx,fruit.cy)<= fruit.r+10
                and distance(app.movement[l][0],app.movement[l][1],fruit.cx,fruit.cy)<= fruit.r+10
                and fruit not in removeable):
                    removeable.append(fruit)
                    
    # temp = set(app.removeable)
    # print(temp)
    for fruit in removeable:
        app.fruits.remove(fruit)

def redrawAll(app):
    for l in range(1,len(app.movement)):
        drawLine(app.movement[l-1][0],app.movement[l-1][1],app.movement[l][0],app.movement[l][1],fill='blue')
    for fruit in app.fruits:
        fruit.cx += fruit.xVelocity
        fruit.cy += fruit.yVelocity
        fruit.yVelocity += 0.5
        drawCircle(fruit.cx,fruit.cy,fruit.r,fill='red')
runApp(width=x,height=y)