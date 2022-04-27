from cmu_cs3_graphics import *
import random
from boids import boids
import math

#this file dictates and manages the fruit, bomb movement and slicing. This mainly
#dictates the normal mode and is overlayed with cs3handTracking.py for hand mode.

class Fruit(object):
    def __init__(self, name, app):
        self.name = name
        self.cx = random.randrange(0, app.width)
        self.cy = app.height
        if self.cx <= app.width/2:
            self.xVelocity = random.randrange(1, 20)
        else:
            self.xVelocity = random.randrange(-20, -1)
        self.yVelocity = random.randint(-app.height//20, -app.height//35)
        self.xAcceleration = 1
        self.yAcceleration = 1
        self.intersect = set()
        self.entryCords = []
        self.exitCords = []
        self.entryPoint = None
        self.exitPoint = None
        self.cords = set()
        self.points = 0


class Apple(Fruit):
    def __init__(self, name, app):
        super().__init__(name, app)
        self.color = 'red'
        self.r = 60
        self.points = 1


class frenzy(Fruit):
    def __init__(self, name, app):
        super().__init__(name, app)
        self.color = 'yellow'
        self.r = 40
        self.cy = 0
        self.xVelocity = 0
        self.yVelocity = 8
        self.xAcceleration = 0
        self.yAcceleration = 2


class slicedFruit(object):
    def __init__(self, p1, p2, height, width, angle, cx, cy, sweepAngle, xA, color, shape):
        self.width = width
        self.p1 = p1
        self.p2 = p2
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
        self.shape = shape


class Bomb(object):
    def __init__(self, app):
        self.cx = random.choice([0, app.width])
        self.cy = random.randrange(0, app.height//2)
        self.xVelocity = app.width/50
        if self.cx == app.width:
            self.xVelocity = -self.xVelocity
        self.yVelocity = -5
        self.xAcceleration = 0
        self.yAcceleration = 1
        self.r = 80
        self.color = 'black'
        self.points = 10
        self.sliceable = True


def onAppStart(app):
    app.fruits = [Apple('First', app)]
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
    app.test = []
    app.r, app.g, app.b = 255, 0, 0
    app.gameOver = False

# reference: https://cs3.academy.cs.cmu.edu/collection/2274/0/exercise


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def cordCalc(p1, p2, cx, cy, r):
    cy = -cy
    if p2[0] != p1[0]:
        gradient = ((-p2[1])-(-p1[1]))/(p2[0]-p1[0])
        c = (-p1[1]) - gradient*p1[0]
        result = []
        x = -(math.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(2*cx*cy-2*cx*c)
              * gradient-(cy**2)+(2*c*cy)-(c**2))+((c-cy)*gradient)-cx)/((gradient**2)+1)
        y = gradient*x+c
        result.append((x, -y))
        x = (math.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(2*cx*cy-2*cx*c)
             * gradient-(cy**2)+(2*c*cy)-(c**2))+((cy-c)*gradient)+cx)/((gradient**2)+1)
        y = gradient*x+c
        result.append((x, -y))
        return result
    else:
        x = p1[0]
        result = []
        y = (-(math.sqrt((-x**2)+2*cx*x+(r**2)-(cx**2))))-cy
        result.append((x, -y))
        y = (math.sqrt((-x**2)+2*cx*x+(r**2)-(cx**2)))-cy
        result.append((x, -y))
        return result


def angleCalc(p1, p2):
    dx = p2[0]-p1[0]
    dy = p1[1] - p2[1]
    if dy != 0:
        angle = math.atan(dx/dy) * 360 / (2*math.pi)
        return angle
    else:
        return None


def radiusCalc(newCx, newCy, cx, cy, r):
    p1 = (newCx, newCy)
    p2 = (cx, cy)
    if p2[0] != p1[0]:
        cy = -cy
        gradient = ((-p2[1])-(-p1[1]))/(p2[0]-p1[0])
        c = (-p1[1]) - gradient*p1[0]
        result = []
        x = -(math.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(2*cx *cy-2*cx*c)*gradient-(cy**2)+(2*c*cy)-(c**2))+((c-cy)*gradient)-cx) /((gradient**2)+1)
        y = gradient*x+c
        result.append((x, -y))
        x = (math.sqrt(((gradient**2)+1)*(r**2)-((cx**2)*(gradient**2))+(2*cx *cy-2*cx*c)*gradient-(cy**2)+(2*c*cy)-(c**2))+((cy-c)*gradient)+cx) /((gradient**2)+1)
        y = gradient*x+c
        result.append((x, -y))
        minY = result[0][1] if result[0][1] < result[1][1] else result[1][1]
        minX = result[0][0] if minY == result[0][1] else result[1][0]
        dis = distance(minX, minY, newCx, newCy)
        return dis
    else:
        return abs(r-abs(newCy-cy))


def onMouseMove(app, mouseX, mouseY):
    if app.gameOver == False:
        app.handX = mouseX
        app.handY = mouseY
        app.movement.append((mouseX, mouseY))
        slicing(app, mouseX, mouseY)


def slicing(app, mouseX, mouseY):
    for fruit in app.fruits:
        for l in range(1, len(app.movement)):
            if (distance(app.movement[l-1][0], app.movement[l-1][1], fruit.cx, fruit.cy) >= fruit.r and
                    distance(app.movement[l][0], app.movement[l][1], fruit.cx, fruit.cy) <= fruit.r):
                fruit.entryCords = (app.movement[l-1], app.movement[l])
                if type(fruit) == frenzy:
                    app.boids = abs(app.boids-1)
            if fruit.entryCords != []:
                app.removeable.add(fruit)
                app.points += fruit.points
                result = cordCalc(
                    fruit.entryCords[0], fruit.entryCords[1], fruit.cx, fruit.cy, fruit.r)
                fruit.entryPoint = result[0]
                fruit.exitPoint = result[1]
                fruit.angle = angleCalc(fruit.entryPoint, fruit.exitPoint)
                newCx = (fruit.entryPoint[0] + fruit.exitPoint[0])/2
                newCy = (fruit.entryPoint[1] + fruit.exitPoint[1])/2
                newRadius = radiusCalc(
                    newCx, newCy, fruit.cx, fruit.cy, fruit.r)
                width = abs(distance(
                    fruit.entryPoint[0], fruit.entryPoint[1], fruit.exitPoint[0], fruit.exitPoint[1]))
                topArc = None
                bottomArc = None
                triangle = None
                xFactor = -20 if newCx <= fruit.cx else 20
                yFactor = -20 if newCy <= fruit.cy else 20
                sweep = 360 - (math.acos(((2*(fruit.r**2))-(width**2)) / (2*(fruit.r**2)))*(180/math.pi))
                if fruit.angle == None:
                    turnAngle = (360-sweep)/2
                    if newRadius < fruit.r:
                        topArc = slicedFruit(fruit.entryPoint,
                                                fruit.exitPoint, 2*newRadius, width, 0, newCx-20, newCy-20, 180,
                                                fruit.xAcceleration, fruit.color, 'arc')

                        bottomArc = slicedFruit(fruit.entryPoint,
                                            fruit.exitPoint, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx+20, fruit.cy+20, sweep,
                                            fruit.xAcceleration, fruit.color, 'barc')

                        triP1 = (fruit.entryPoint[0] +20, fruit.entryPoint[1] +20)
                        triP2 = (fruit.exitPoint[0] +20, fruit.exitPoint[1] +20)
                        triangle = slicedFruit(triP1,triP2, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx +
                                                20, fruit.cy +20, sweep,
                                                fruit.xAcceleration, fruit.color, 'tri')

                    elif newRadius > fruit.r:
                        turnAngle +=180
                        topArc = slicedFruit(fruit.entryPoint,
                                                fruit.exitPoint, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx+20, fruit.cy+20, sweep,
                                                fruit.xAcceleration, fruit.color, 'barc')
                        bottomArc = slicedFruit(fruit.entryPoint,
                                                fruit.exitPoint, (2*fruit.r-newRadius)*2, width, 180, newCx-20, newCy-20, sweep,
                                                fruit.xAcceleration, fruit.color, 'arc')
                        triP1 = (fruit.entryPoint[0] +20, fruit.entryPoint[1] +20)
                        triP2 = (fruit.exitPoint[0] +20, fruit.exitPoint[1] +20)
                        triangle = slicedFruit(triP1,triP2, 2*fruit.r, 2*fruit.r, turnAngle,
                                                fruit.cx+20, fruit.cy+20, sweep,
                                                fruit.xAcceleration, fruit.color, 'tri')

                        
                else:
                    turnAngle = fruit.angle-((180-(360-sweep))/2)
                    if fruit.angle <= 0:
                        if newRadius < fruit.r:
                            topArc = slicedFruit(fruit.entryPoint,
                                                 fruit.exitPoint, newRadius*2, width, 90 +
                                                 fruit.angle, newCx+xFactor, newCy+yFactor, 180,
                                                 fruit.xAcceleration, fruit.color, 'arc')

                            turnAngle -= 180
                            if turnAngle < 0:
                                turnAngle += 360
                            bottomArc = slicedFruit(fruit.entryPoint,
                                                    fruit.exitPoint, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx -
                                                    xFactor, fruit.cy-yFactor, sweep,
                                                    fruit.xAcceleration, fruit.color, 'barc')

                            triP1 = (fruit.entryPoint[0] - xFactor, fruit.entryPoint[1] - yFactor)
                            triP2 = (fruit.exitPoint[0] - xFactor, fruit.exitPoint[1] - yFactor)
                            triangle = slicedFruit(triP1,triP2, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx -
                                                   xFactor, fruit.cy - yFactor, sweep,
                                                   fruit.xAcceleration, fruit.color, 'tri')

                        elif newRadius > fruit.r:
                            bottomArc = slicedFruit(fruit.entryPoint,
                                                    fruit.exitPoint, (2*fruit.r-newRadius)*2,
                                                    width, fruit.angle-90, newCx+xFactor, newCy+yFactor, 180,
                                                    fruit.xAcceleration, fruit.color, 'arc')

                            topArc = slicedFruit(fruit.entryPoint,
                                                 fruit.exitPoint, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx -xFactor,
                                                 fruit.cy-yFactor, sweep,
                                                 fruit.xAcceleration, fruit.color, 'barc')

                            triP1 = (fruit.entryPoint[0] - xFactor, fruit.entryPoint[1] - yFactor)
                            triP2 = (fruit.exitPoint[0] - xFactor, fruit.exitPoint[1] - yFactor)
                            triangle = slicedFruit(triP1,triP2, 2*fruit.r, 2*fruit.r, turnAngle,
                                                    fruit.cx-xFactor, fruit.cy-yFactor, sweep,
                                                   fruit.xAcceleration, fruit.color, 'tri')

                    elif newRadius < fruit.r:
                        topArc = slicedFruit(fruit.entryPoint,
                                             fruit.exitPoint, newRadius*2, width, 270 +
                                             fruit.angle, newCx+xFactor, newCy+yFactor, 180,
                                             fruit.xAcceleration, fruit.color, 'arc')

                        bottomArc = slicedFruit(fruit.entryPoint,
                                                fruit.exitPoint, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx -xFactor,
                                                fruit.cy-yFactor, sweep,
                                                fruit.xAcceleration, fruit.color, 'barc')

                        triP1 = (
                            fruit.entryPoint[0] - xFactor, fruit.entryPoint[1] - yFactor)
                        triP2 = (fruit.exitPoint[0] - xFactor,
                                 fruit.exitPoint[1] - yFactor)
                        triangle = slicedFruit(triP1,triP2, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx-xFactor,
                                               fruit.cy+20, sweep,fruit.xAcceleration, fruit.color, 'tri')

                    elif newRadius > fruit.r:
                        bottomArc = slicedFruit(fruit.entryPoint,fruit.exitPoint,(2*fruit.r-newRadius)*2,
                                                width, 90+fruit.angle, newCx+xFactor, newCy+yFactor, 180,
                                                fruit.xAcceleration, fruit.color, 'arc')

                        turnAngle += 180
                        topArc = slicedFruit(fruit.entryPoint,
                                             fruit.exitPoint, 2*fruit.r, 2*fruit.r, turnAngle, fruit.cx -xFactor,
                                             fruit.cy-yFactor, sweep,
                                             fruit.xAcceleration, fruit.color, 'barc')

                        triP1 = (
                            fruit.entryPoint[0] - xFactor, fruit.entryPoint[1] - yFactor)
                        triP2 = (fruit.exitPoint[0] - xFactor,
                                 fruit.exitPoint[1] - yFactor)
                        triangle = slicedFruit(triP1,triP2, 2*fruit.r, 2*fruit.r, turnAngle,
                                               fruit.cx-xFactor, fruit.cy-yFactor, sweep,
                                               fruit.xAcceleration, fruit.color, 'tri')

                    else:
                        bottomArc = slicedFruit(fruit.entryPoint,fruit.exitPoint, 2*fruit.r, width,
                                                90 +fruit.angle, newCx-xFactor, newCy-yFactor, 180,
                                                fruit.xAcceleration, fruit.color, 'arc')

                        topArc = slicedFruit(fruit.entryPoint,fruit.exitPoint, 2*fruit.r, width,
                                             270 +fruit.angle, newCx+xFactor, newCy+yFactor, 180,
                                             fruit.xAcceleration, fruit.color, 'arc')
                if topArc != None:
                    app.slicedFruits.append(topArc)
                if bottomArc != None:
                    app.slicedFruits.append(bottomArc)
                if triangle != None:
                    app.slicedFruits.append(triangle)

    for bomb in app.bombs:
        if bomb.sliceable == True:
            if distance(bomb.cx, bomb.cy, mouseX, mouseY) <= bomb.r:
                app.gameOver = True
                bomb.xVelocity = 0
                bomb.yVelocity = -10
                bomb.sliceable = False

    for fruit in app.removeable:
        app.fruits.remove(fruit)
    app.removeable = set()


def onStep(app):
    if app.g < 255:
        app.g += 5
    elif app.b < 255:
        app.b += 5
    if app.g >= 255 and app.b >= 255:
        app.g = 0
        app.b = 0
    if app.gameOver == False:
        app.count += 1
        if app.count % 30 == 0 and not bool(app.boids):
            app.fruits.append(Apple(str(app.count), app))
        if app.count % 5 == 0:
            app.movement = []
        if app.count % 300 == 0 and bool(app.boids) == False:
            app.bombs.append(Bomb(app))
        if app.count >= app.frenzyCount:
            if bool(app.boids) == False:
                app.fruits.append(frenzy('n', app))
            app.frenzyCount = random.randrange(app.count, app.count+200)
        if app.points < 0:
            app.gameOver = True
    if bool(app.boids):
        if app.boidsCount >= 100:
            app.boidsCount = 0
            app.boids = abs(app.boids-1)
        else:
            if app.boidsCount % 5 == 0:
                app.fruits.append(Apple(str(app.count), app))
            app.fruits = boids(app.fruits, app.width, app.height)
        app.boidsCount += 1
    else:
        for fruit in app.fruits:
            fruit.cx += fruit.xVelocity
            fruit.cy += fruit.yVelocity
            if fruit.xVelocity < 0:
                fruit.xVelocity -= fruit.xAcceleration
            else:
                fruit.xVelocity += fruit.xAcceleration
            fruit.yVelocity += fruit.yAcceleration
            fruit.intersect = set()
            fruit.entryPoint = None
            fruit.exitPoint = None
            if fruit.cx > app.width or fruit.cx < 0 or fruit.cy > app.height or fruit.cy < 0:
                app.removeable.add(fruit)
    removeableBomb = set()
    for bomb in app.bombs:
        if bomb.cx > app.width or bomb.cx < 0 or bomb.cy > app.height or bomb.cy < 0:
            removeableBomb.add(bomb)
    for bomb in removeableBomb:
        app.bombs.remove(bomb)
    for fruit in app.slicedFruits:
        fruit.cx += fruit.xVelocity
        fruit.cy += fruit.yVelocity
        if fruit.shape == 'tri':
            fruit.p1 = (fruit.p1[0] + fruit.xVelocity,
                        fruit.p1[1] + fruit.yVelocity)
            fruit.p2 = (fruit.p2[0] + fruit.xVelocity,
                        fruit.p2[1] + fruit.yVelocity)
        if fruit.xVelocity < 0:
            fruit.xVelocity -= fruit.xAcceleration
        else:
            fruit.xVelocity += fruit.xAcceleration

        fruit.yVelocity += fruit.yAcceleration
        if fruit.cx > app.width or fruit.cx < 0 or fruit.cy > app.height or fruit.cy < 0:
            app.removeable.add(fruit)
    for bomb in app.bombs:
        bomb.yVelocity += bomb.yAcceleration
        bomb.cx += bomb.xVelocity
        bomb.cy += bomb.yVelocity
    for fruit in app.removeable:
        if fruit in app.fruits:
            app.fruits.remove(fruit)
        elif fruit in app.slicedFruits:
            app.slicedFruits.remove(fruit)
    app.removeable = set()
    if app.gameOver:
        app.boids = 0


def redrawAll(app):
    for fruit in app.fruits:
        drawCircle(fruit.cx, fruit.cy, fruit.r, fill=fruit.color)
    for fruit in app.slicedFruits:
        if fruit.shape == 'arc':
            drawArc(fruit.cx, fruit.cy, fruit.width, fruit.height, 270,
                    fruit.sweepAngle, fill=fruit.color, rotateAngle=fruit.angle)
        elif fruit.shape == 'barc':
            drawArc(fruit.cx, fruit.cy, fruit.width, fruit.height, fruit.angle,
                    fruit.sweepAngle, fill=fruit.color)
        elif fruit.shape == 'tri':
            drawPolygon(
                fruit.cx, fruit.cy, fruit.p1[0], fruit.p1[1], fruit.p2[0], fruit.p2[1], fill=fruit.color)
    drawLabel('Points: '+str(app.points), app.width -
              100, 30, size=app.height/20, fill=rgb(app.r, app.g, app.b))
    for bomb in app.bombs:
        drawCircle(bomb.cx, bomb.cy, bomb.r, fill=bomb.color)
    if app.gameOver == False:
        if app.status == 'normal':
            for l in range(1, len(app.movement)):
                drawLine(app.movement[l-1][0], app.movement[l-1][1],
                         app.movement[l][0], app.movement[l][1], fill='blue')
        if bool(app.boids):
            drawLabel('FRENZY!', app.width//2, 100, size=100,
                      fill='yellow', align='center')
    else:
        drawLabel('Game Over', app.width//2, app.height//2,
                  size=100, fill=rgb(app.r, app.g, app.b))


if __name__ == '__main__':
    runApp(width=1280, height=720)
