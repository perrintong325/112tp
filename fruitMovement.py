from cmu_cs3_graphics import *
import random
from boids import boids
import math
import cmath
import sympy

# x, y = app.width, app.height


class Fruit(object):
    def __init__(self, name,app):
        self.name = name
        self.cx = random.randrange(0, app.width)
        self.cy = app.height
        self.xVelocity = random.randrange(-20, 20)
        self.yVelocity = random.randint(-app.height//25, -app.height//35)
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
    def __init__(self, name,app):
        super().__init__(name,app)
        self.color = 'red'
        self.r = 60
        # self.draw = f'drawCircle({self.cx}, {self.cy}, {self.r}, {self.color})'
        self.points = 1

class frenzy(Fruit):
    def __init__(self, name,app):
        super().__init__(name,app)
        self.color = 'yellow'
        self.r = 30
        self.cy = 0
        self.xVelocity = 0
        self.yVelocity = 20
        self.xAcceleration = 0
        self.yAcceleration = 5
        self.points = 0
    

class slicedFruit(object):
    def __init__(self, p1,p2,height,angle,cx,cy,sweepAngle,xV,yV,xA,yA,color):
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
        self.color = color


class Bomb(object):
    def __init__(self,app):
        self.cx = random.choice([0, app.width])
        self.cy = random.randrange(0, app.height)
        self.xVelocity = app.width/20
        self.yVelocity = -5
        self.xAcceleration = 0
        self.yAcceleration = 9.8
        self.r = 10
        self.color = 'black'
        self.points = 10
        

def onAppStart(app):  
    app.fruits = [Apple('First',app)]
    app.slicedFruits = []
    app.bombs = []
    app.count = 0
    app.removeable = set()
    app.handX = -1
    app.handY = -1
    app.movement = []
    app.moveCount = 0
    app.boids = 0
    app.points = 0
    app.frenzyCount = random.randrange(0, 30)
    app.boidsCount = 0

# reference: cs academy


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def cordCalc(p1, p2, cx, cy,r):
    if p2[0] != p1[0]:
        gradient = (p2[1]-p1[1])/(p2[0]-p1[0])
        c = p1[1] - gradient*p1[0]
        result = []
        x = (cmath.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(((2*cx*cy)-(2*cx*c))*gradient)-(c**2)+(2*cy*c)-(cy**2))+((c-cy)*gradient)+cx)/((gradient**2)+1)
        y = gradient*x + c
        result.append((abs(x),abs(y)))
        x = -(cmath.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(((2*cx*cy)-(2*cx*c))*gradient)-(c**2)+(2*cy*c)-(cy**2))+((c-cy)*gradient)-cx)/((gradient**2)+1)
        y = gradient*x + c
        result.append((abs(x),abs(y)))
        return result
        # x,y = sympy.symbols('x,y')
        # eq1 = sympy.Eq((x-cx)**2+(y-cy)**2,r**2)
        # eq2 = sympy.Eq(gradient*x+c,y)
        # result = sympy.solve([eq1,eq2],(x,y))
    #     newResult = []
    #     for x in result:
    #         newResult.append([abs(x[0]),abs(x[1])])
    #     return (abs(result[0][0]),abs(result[0][1]))
    # else:
    #     y = cy - math.sqrt(((-(p1[0]))**2)+(2*cx*p1[0])+(r**2)-(cx**2))
    #     return (p1[0],y)
    # c = smallY - gradient*smallX
    # pointX,pointY = 0,0
    # while smallX <= largeX or smallY <= largeY:
    #     if distance(smallX, smallY, cx, cy) == r:
    #         print(smallX, smallY)
    #     else:
    #         smallY = smallX*gradient + c
    #         smallX += 1
    return p1

def angleCalc(p1,p2):
    return 90 -((math.atan2(p2[1]-p1[1], p2[0]-p1[0]))*360/(2*math.pi))

def radiusCalc(newCx, newCy, cx, cy, r):
    return r - distance(newCx, newCy, cx, cy)

def onMouseMove(app,mouseX,mouseY):
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
                app.points += fruit.points
                # fruit.entryPoint = cordCalc(fruit.entryCords[0], fruit.entryCords[1], fruit.cx+160, fruit.cy,fruit.r)
                # fruit.exitPoint = cordCalc(fruit.exitCords[0], fruit.exitCords[1], fruit.cx, fruit.cy,fruit.r)
                result = cordCalc(fruit.entryCords[0], fruit.entryCords[1], fruit.cx+160, fruit.cy+160,fruit.r)
                fruit.entryPoint = result[1]
                fruit.exitPoint = result[0]
                fruit.angle = angleCalc(fruit.entryPoint, fruit.exitPoint)
                newCx = (fruit.entryPoint[0] + fruit.exitPoint[0])/2
                newCy = (fruit.entryPoint[1] + fruit.exitPoint[1])/2
                newRadius = radiusCalc(newCx, newCy, fruit.cx, fruit.cy, fruit.r)
                app.slicedFruits.append(slicedFruit(fruit.entryPoint,
                    fruit.exitPoint, newRadius, fruit.angle, newCx+5, newCy,180,
                    fruit.xVelocity, fruit.yVelocity, fruit.xAcceleration,
                    fruit.yAcceleration,fruit.color))
                app.slicedFruits.append(slicedFruit(fruit.entryPoint,
                    fruit.exitPoint, newRadius, fruit.angle+180, newCx-5,
                    newCy,180, fruit.xVelocity, fruit.yVelocity,
                    fruit.xAcceleration,fruit.yAcceleration,fruit.color))
                if type(fruit) == frenzy:
                    app.boids = abs(app.boids-1)
                # print(fruit.entryPoint, fruit.exitPoint)
    for bomb in app.bombs:
        if distance(bomb.cx, bomb.cy, mouseX, mouseY) <= bomb.r:
            app.points -= bomb.points

    for fruit in app.removeable:
        app.fruits.remove(fruit)
    app.removeable = set()

def onKeyPress(app,key):
    if key == 'space':
        app.boids = abs(app.boids-1)


def onStep(app):
    app.count += 1
    if app.count % 10 == 0:
        app.fruits.append(Apple(str(app.count),app))
        app.movement = []
    if app.count % 10 == 0 and bool(app.boids) == False:
        app.bombs.append(Bomb(app))
    if app.count >= app.frenzyCount:
        if bool(app.boids) == False:
            app.fruits.append(frenzy('n',app))
        app.frenzyCount = random.randrange(app.count,app.count+30)
    print(app.count, app.frenzyCount)
    if bool(app.boids):
        if app.boidsCount >=200:
            app.boidsCount = 0
            app.boids = abs(app.boids-1)
        else:
            app.fruits = boids(app.fruits,app.width,app.height)
        app.boidsCount += 1
    else:
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
    for bomb in app.bombs:
        bomb.cx += bomb.xVelocity
        bomb.cy += bomb.yVelocity
    for fruit in app.removeable:
        if fruit in app.fruits:
            app.fruits.remove(fruit)
        elif fruit in app.slicedFruits:
            app.slicedFruits.remove(fruit)
    app.removeable = set()


def redrawAll(app):
    for fruit in app.fruits:
        drawCircle(fruit.cx, fruit.cy, fruit.r, fill=fruit.color)
        # drawLabel(fruit.name, fruit.cx, fruit.cy)
    for fruit in app.slicedFruits:
        drawArc(int(fruit.cx), int(fruit.cy), int(fruit.width),int(fruit.height), fruit.angle,fruit.sweepAngle, fill=fruit.color)
    for bomb in app.bombs:
        drawCircle(bomb.cx, bomb.cy, bomb.r, fill=bomb.color)
    if app.status == 'normal':
        for l in range(1, len(app.movement)):
            drawLine(app.movement[l-1][0], app.movement[l-1][1],
                    app.movement[l][0], app.movement[l][1], fill='blue')
    if bool(app.boids):
        drawLabel('FRENZY!', app.width//2, 100,size = 100,fill='yellow',align='center')
    drawLabel('Points: '+str(app.points), app.width-100, 30,size=app.height/20,fill = 'purple')
        

if __name__ == '__main__':
    runApp(width=1280, height=720)
