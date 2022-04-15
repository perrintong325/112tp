from cmu_cs3_graphics import *
import random
from boids import boids

x, y = 1920, 1080
# temporary test class


class Fruit(object):
    def __init__(self, name):
        self.name = name
        self.cx = random.randrange(0, x)
        self.cy = y
        self.xVelocity = random.randrange(-20, 10)
        self.yVelocity = random.randint(-y//30, -y//50)
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
        self.r = 20
        self.draw = f'drawCircle({self.cx}, {self.cy}, {self.r}, {self.color})'

class slicedFruit(object):
    def __init__(self, cords):
        self.cord = ''
        for cord in cords:
            self.cord += f'{cord[0]}, {cord[1]}, '
        self.cord = self.cord[:-2]
        print(self.cord)


class Bomb(object):
    def __init__(self):
        self.cx = random.randrange(0, x)
        self.cy = y
        self.xVelocity = random.randrange(-1, 1)
        self.yVelocity = 5
        self.r = 10
        self.color = 'red'
        

def onAppStart(app):
    app.fruits = [Apple('First')]
    app.slicedFruits = []
    app.bombs = []
    app.count = 0
    app.removeable = set()
    app.handX = -1
    app.handY = -1
    app.movement = []
    app.moveCount = 0
    # app.stepsPerSecond = 3
    app.boids = 0

# reference: cs academy


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def cordCalc(p1, p2, cx, cy,r):
    smallX = min(p1[0], p2[0])
    largeX = max(p1[0], p2[0])
    smallY = min(p1[1], p2[1])
    largeY = max(p1[1], p2[1])
    gradient = (p2[1]-p1[1])/(p2[0]-p1[0])
    c = smallY - gradient*smallX
    pointX,pointY = 0,0
    while smallX <= largeX or smallY <= largeY:
        if distance(smallX, smallY, cx, cy) == r:
            print(smallX, smallY)
        else:
            smallY = smallX*gradient + c
            smallX += 1

def onMouseMove(app, mouseX, mouseY):
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
                app.slicedFruits.append(slicedFruit(fruit.cords))
                # fruit.entryPoint = cordCalc(fruit.entryCords[0], fruit.entryCords[1], fruit.cx, fruit.cy,fruit.r)
                # fruit.exitPoint = cordCalc(fruit.exitCords[0], fruit.exitCords[1], fruit.cx, fruit.cy,fruit.r)
                # print(fruit.entryPoint, fruit.exitPoint)

    for fruit in app.removeable:
        app.fruits.remove(fruit)
    app.removeable = set()

def onKeyPress(app,key):
    if key == 'space':
        app.boids = abs(app.boids-1)


def onStep(app):
    app.count += 1
    if app.count % 10 == 0:
        app.fruits.append(Apple(str(app.count)))
    if app.count % 20 == 0:
        app.bombs.append(Bomb())
    app.movement = []
    if bool(app.boids) == False:
        for fruit in app.fruits:
            fruit.cx += fruit.xVelocity
            fruit.cy += fruit.yVelocity
            fruit.yVelocity += 0.5
            fruit.intersect = set()
            fruit.entryPoint = None
            fruit.exitPoint = None
            if fruit.cx > app.width or fruit.cx < 0 or fruit.cy > app.height or fruit.cy < 0:
                app.removeable.add(fruit)
    else:
        app.fruits = boids(app.fruits,x,y)
    for bomb in app.bombs:
        bomb.cx += bomb.xVelocity
        bomb.cy += bomb.yVelocity
    for fruit in app.removeable:
        app.fruits.remove(fruit)
    app.removeable = set()


def redrawAll(app):
    for fruit in app.fruits:
        drawCircle(fruit.cx, fruit.cy, fruit.r, fill='red')
        drawLabel(fruit.name, fruit.cx, fruit.cy)
    for fruit in app.slicedFruits:
        eval(f"drawPolygon({fruit.cord}, fill='green')")
    for bomb in app.bombs:
        drawCircle(bomb.cx, bomb.cy, bomb.r, fill='red')
    for l in range(1, len(app.movement)):
        drawLine(app.movement[l-1][0], app.movement[l-1][1],
                app.movement[l][0], app.movement[l][1], fill='blue')
        

if __name__ == '__main__':
    runApp(width=x, height=y)
