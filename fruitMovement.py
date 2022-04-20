from cmu_cs3_graphics import *
import random
from boids import boids
import math
import sympy

x, y = 1920, 1080


class Fruit(object):
    def __init__(self, name):
        self.name = name
        self.cx = random.randrange(0, x)
        self.cy = y
        self.xVelocity = random.randrange(-15, 15)
        self.yVelocity = random.randint(-y//30, -y//45)
        self.xAcceleration = 1
        self.yAcceleration = 1
        # self.r = random.randrange(5,15)
        # self.r = 20
        self.intersect = set()
        self.entryCords = None
        self.exitCords = None
        self.entryPoint = None
        self.exitPoint = None
        self.cords = set()
        
    
class Apple(Fruit):
    def __init__(self, name):
        super().__init__(name)
        self.color = 'red'
        self.r = 40
        self.draw = f'drawCircle({self.cx}, {self.cy}, {self.r}, {self.color})'

class slicedFruit(object):
    def __init__(self, p1,p2,height,angle,cx,cy,sweepAngle,xV,yV,xA,yA):
        self.width = abs(distance(p1[0],p1[1],p2[0],p2[1]))
        self.cx = cx
        self.cy = cy
        self.height = abs(height)
        self.angle = angle
        self.sweepAngle = sweepAngle
        self.xVelocity = 0
        self.yVelocity = -10
        self.xAcceleration = xA
        self.yAcceleration = 3


class Bomb(object):
    def __init__(self):
        self.cx = random.randrange(0, x)
        self.cy = y
        self.xVelocity = random.randrange(-1, 1)
        self.yVelocity = 5
        self.r = 10
        self.color = 'red'
        

#def onAppStart(app):
def fruitMovementOnAppStart(app):    
    app.fruits = [Apple('First')]
    app.slicedFruits = []
    app.bombs = []
    app.count = 0
    app.removeable = set()
    app.handX = -1
    app.handY = -1
    app.movement = []
    app.moveCount = 0
    app.stepsPerSecond = 120
    app.boids = 0

# reference: cs academy


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def cordCalc(p1, p2, cx, cy,r):
    # smallX = min(p1[0], p2[0])
    # largeX = max(p1[0], p2[0])
    # smallY = min(p1[1], p2[1])
    # largeY = max(p1[1], p2[1])
    if p2[0] != p1[0]:
        gradient = (p2[1]-p1[1])/(p2[0]-p1[0])
        c = p1[1] - gradient*p1[0]
        # x = (math.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(((2*cx*cy)-(2*cx*c))*gradient)-(c**2)+(2*cy*c)-(cy**2))+((c-cy)*gradient)-cx)/((gradient**2)+1)
        #y = gradient*x + c
        #return (x,y)
        x,y = sympy.symbols('x,y')
        eq1 = sympy.Eq((x-cx)**2+(y-cy)**2,r**2)
        eq2 = sympy.Eq(gradient*x+c,y)
        result = sympy.solve([eq1,eq2],(x,y))
        print(result)
        newResult = []
        for x in result:
            newResult.append([abs(x[0]),abs(x[1])])
        return (abs(result[0][0]),abs(result[0][1]))
    else:
        y = cy - math.sqrt(((-(p1[0]))**2)+(2*cx*p1[0])+(r**2)-(cx**2))
        return (p1[0],y)
    # c = smallY - gradient*smallX
    # pointX,pointY = 0,0
    # while smallX <= largeX or smallY <= largeY:
    #     if distance(smallX, smallY, cx, cy) == r:
    #         print(smallX, smallY)
    #     else:
    #         smallY = smallX*gradient + c
    #         smallX += 1
    return (x,y)
    # return((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def angleCalc(p1,p2):
    return 90 -((math.atan2(p2[1]-p1[1], p2[0]-p1[0]))*360/(2*math.pi))

def radiusCalc(newCx, newCy, cx, cy, r):
    return r - distance(newCx, newCy, cx, cy)

# def onMouseMove(app, mouseX, mouseY):
def fruitMovementOnMouseMove(app,mouseX,mouseY):
    app.handX = mouseX
    app.handY = mouseY
    app.movement.append((mouseX, mouseY))
    for fruit in app.fruits:
        for l in range(1, len(app.movement)):
            if (distance(app.movement[l-1][0], app.movement[l-1][1], fruit.cx, fruit.cy) >= fruit.r and
                    distance(app.movement[l][0], app.movement[l][1], fruit.cx, fruit.cy) <= fruit.r):
                fruit.entryCords = (app.movement[l-1], app.movement[l])
            elif (distance(app.movement[l-1][0], app.movement[l-1][1], fruit.cx, fruit.cy) <= fruit.r and
                    distance(app.movement[l][0], app.movement[l][1], fruit.cx, fruit.cy) >= fruit.r):
                fruit.exitCords = (app.movement[l-1], app.movement[l])
            elif fruit.entryCords != None and fruit.exitCords == None:
                fruit.cords.add((mouseX, mouseY))
            if fruit.exitCords != None and fruit.entryCords != None:
                app.removeable.add(fruit)
                fruit.entryPoint = cordCalc(fruit.entryCords[0], fruit.entryCords[1], fruit.cx+160, fruit.cy,fruit.r)
                fruit.exitPoint = cordCalc(fruit.exitCords[0], fruit.exitCords[1], fruit.cx, fruit.cy,fruit.r)
                # result = cordCalc(fruit.entryCords[0], fruit.entryCords[1], fruit.cx+160, fruit.cy+160,fruit.r)
                # fruit.entryPoint = result[0]
                # fruit.exitPoint = result[1]
                print("point:", fruit.entryPoint, fruit.exitPoint)
                fruit.angle = angleCalc(fruit.entryPoint, fruit.exitPoint)
                newCx = (fruit.entryPoint[0] + fruit.exitPoint[0])/2
                newCy = (fruit.entryPoint[1] + fruit.exitPoint[1])/2
                newRadius = radiusCalc(newCx, newCy, fruit.cx, fruit.cy, fruit.r)
                app.slicedFruits.append(slicedFruit(fruit.entryPoint,
                    fruit.exitPoint, newRadius, fruit.angle, newCx+5, newCy,180,
                    fruit.xVelocity, fruit.yVelocity, fruit.xAcceleration,
                    fruit.yAcceleration))
                app.slicedFruits.append(slicedFruit(fruit.entryPoint,
                    fruit.exitPoint, newRadius, fruit.angle+180, newCx-5,
                    newCy,180, fruit.xVelocity, fruit.yVelocity,
                    fruit.xAcceleration,fruit.yAcceleration))
                # print(fruit.entryPoint, fruit.exitPoint)

    for fruit in app.removeable:
        app.fruits.remove(fruit)
    app.removeable = set()

def onKeyPress(app,key):
    if key == 'space':
        app.boids = abs(app.boids-1)


# def onStep(app):
def fruitMovementOnStep(app):
    app.count += 1
    if app.count % 10 == 0:
        app.fruits.append(Apple(str(app.count)))
        app.movement = []
    if app.count % 20 == 0:
        app.bombs.append(Bomb())
    if bool(app.boids) == False:
        for fruit in app.fruits:
            fruit.cx += fruit.xVelocity
            fruit.cy += fruit.yVelocity
            if fruit.xVelocity <0:
                fruit.xVelocity -= fruit.xAcceleration
            else:
                fruit.xVelocity += fruit.xAcceleration
            fruit.yVelocity += fruit.yAcceleration
            fruit.intersect = set()
            fruit.entryPoint = None
            fruit.exitPoint = None
            if fruit.cx > app.width or fruit.cx < 0 or fruit.cy > app.height or fruit.cy < 0:
                app.removeable.add(fruit)
        for fruit in app.slicedFruits:
            fruit.cx += fruit.xVelocity
            fruit.cy += fruit.yVelocity
            if fruit.xVelocity <0:
                fruit.xVelocity -= fruit.xAcceleration
            else:
                fruit.xVelocity += fruit.xAcceleration
            fruit.yVelocity += fruit.yAcceleration
            if fruit.cx > app.width or fruit.cx < 0 or fruit.cy > app.height or fruit.cy < 0:
                app.removeable.add(fruit)
    else:
        app.fruits = boids(app.fruits,x,y)
    for bomb in app.bombs:
        bomb.cx += bomb.xVelocity
        bomb.cy += bomb.yVelocity
    for fruit in app.removeable:
        if fruit in app.fruits:
            app.fruits.remove(fruit)
        elif fruit in app.slicedFruits:
            app.slicedFruits.remove(fruit)
    app.removeable = set()


# def redrawAll(app):
def fruitMovementRedrawAll(app):
    for fruit in app.fruits:
        drawCircle(fruit.cx, fruit.cy, fruit.r, fill='red')
        drawLabel(fruit.name, fruit.cx, fruit.cy)
    for fruit in app.slicedFruits:
        drawArc(int(fruit.cx), int(fruit.cy), int(fruit.width),int(fruit.height), fruit.angle,fruit.sweepAngle, fill='red')
    for bomb in app.bombs:
        drawCircle(bomb.cx, bomb.cy, bomb.r, fill='red')
    for l in range(1, len(app.movement)):
        drawLine(app.movement[l-1][0], app.movement[l-1][1],
                app.movement[l][0], app.movement[l][1], fill='blue')
        

if __name__ == '__main__':
    runApp(width=x, height=y)
