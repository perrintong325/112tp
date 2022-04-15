import math
# from fruitMovement import distance

#reference: stanford cs notes and vergnet boids seudocode
maxSpeed = 20
minSpeed = 10
def boids(fruits,x,y):
    cohesion(fruits)
    seperation(fruits)
    alignment(fruits)
    for fruit in fruits:
        # fruit.xVelocity += fruit.xAcceleration
        # fruit.yVelocity += fruit.yAcceleration
        speed = math.sqrt(fruit.xVelocity**2 + fruit.yVelocity**2)
        if speed > maxSpeed:
            fruit.xVelocity *= maxSpeed/speed
            fruit.yVelocity *= maxSpeed/speed
        elif speed < minSpeed:
            fruit.xVelocity *= minSpeed/speed
            fruit.yVelocity *= minSpeed/speed
        fruit.cx += fruit.xVelocity
        fruit.cy += fruit.yVelocity

    bound(fruits,x,y)
    return fruits

# reference: cs academy


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def cohesion(fruits):
    # cx = 0
    # cy = 0
    # for fruit in fruits:
    #     cx += fruit.cx
    #     cy += fruit.cy
    # cx /= len(fruits)
    # cy /= len(fruits)
    # for fruit in fruits:
    #     # fruit.perceivedCx = (cx-fruit.cx)/(len(fruits)-1)
    #     # fruit.perceivedCy = (cy-fruit.cy)/(len(fruits)-1)
    #     # fruit.cx += (fruit.perceivedCx - fruit.cx)/50
    #     # fruit.cy += (fruit.perceivedCy - fruit.cy)/50
    #     steerX = cx - fruit.cx - fruit.xVelocity
    #     steerY = cy - fruit.cy - fruit.yVelocity
    #     fruit.xAcceleration += steerX
    #     fruit.yAcceleration += steerY
    centeringFactor = 0.05
    for fruitA in fruits:
        cx = 0
        cy = 0
        neighborCount = 0
        for fruitB in fruits:
            if fruitA != fruitB:
                if distance(fruitA.cx, fruitA.cy, fruitB.cx, fruitB.cy) < fruitA.r+fruitB.r + 40:
                    cx += fruitB.cx
                    cy += fruitB.cy
                    neighborCount += 1
        if neighborCount > 0:
            cx /= neighborCount
            cy /= neighborCount
            fruitA.xVelocity += (cx - fruitA.cx) * centeringFactor
            fruitA.yVelocity += (cy - fruitA.cy) * centeringFactor


def seperation(fruits):
    avoidfactor = 5
    for fruitA in fruits:
        disX = 0
        disY = 0
        for fruitB in fruits:
            if fruitA != fruitB:
                if distance(fruitA.cx, fruitA.cy, fruitB.cx, fruitB.cy) < fruitA.r+fruitB.r + 20:
                    disX += fruitA.cx - fruitB.cx
                    disY += fruitA.cy - fruitB.cy
        fruitA.xVelocity += disX*avoidfactor
        fruitA.yVelocity += disY*avoidfactor

def alignment(fruits):
    # vx = 0
    # vy = 0
    # for fruit in fruits:
    #     vx += fruit.xVelocity
    #     vy += fruit.yVelocity
    # vx /= len(fruits)
    # vy /= len(fruits)
    # for fruit in fruits:
    #     # fruit.perceivedVx = (vx-fruit.xVelocity)/(len(fruits)-1)
    #     # fruit.perceivedVy = (vy-fruit.yVelocity)/(len(fruits)-1)
    #     # fruit.xVelocity += (fruit.perceivedVx - fruit.xVelocity)/20
    #     # fruit.yVelocity += (fruit.perceivedVy - fruit.yVelocity)/20
    #     steerX = vx - fruit.xVelocity
    #     steerY = vy - fruit.yVelocity
    #     fruit.xAcceleration += steerX
    #     fruit.yAcceleration += steerY
    matchingFactor = 5
    for fruitA in fruits:
        vx = 0
        vy = 0
        neighborCount = 0
        for fruitB in fruits:
            if distance(fruitA.cx, fruitA.cy, fruitB.cx, fruitB.cy) < fruitA.r+fruitB.r + 40:
                vx += fruitB.xVelocity
                vy += fruitB.yVelocity
                neighborCount += 1
        if neighborCount > 0:
            vx /= neighborCount
            vy /= neighborCount
            fruitA.xVelocity += vx * matchingFactor
            fruitA.yVelocity += vy * matchingFactor

def bound(fruits,x,y):
    turnFactor = 5
    for fruit in fruits:
        if fruit.cx <= 50:
            fruit.xVelocity += turnFactor
        elif x-50 <= fruit.cx:
            fruit.xVelocity -= turnFactor
        if fruit.cy <= 15:
            fruit.yVelocity += turnFactor
        elif y-15 <= fruit.cy:
            fruit.yVelocity -= turnFactor