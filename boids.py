import math
#this file is used to calculate the movement using boids algorithim when activated

#reference: stanford cs notes, cornell ece notes and vergnet boids seudocode
#https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/modeling-natural-systems/boids.html
#http://www.vergenet.net/~conrad/boids/pseudocode.html
#http://people.ece.cornell.edu/land/courses/ece4760/labs/s2021/Boids/Boids.html
maxSpeed = 40
minSpeed = 5
def boids(fruits,x,y):
    cohesion(fruits)
    seperation(fruits)
    alignment(fruits)
    for fruit in fruits:
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

# reference: https://cs3.academy.cs.cmu.edu/collection/2274/0/exercise


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def cohesion(fruits):
    centeringFactor = 0.005
    for fruitA in fruits:
        cx = 0
        cy = 0
        neighborCount = 0
        for fruitB in fruits:
            if fruitA != fruitB:
                if distance(fruitA.cx, fruitA.cy, fruitB.cx, fruitB.cy) < fruitA.r+fruitB.r+50:
                    cx += fruitB.cx
                    cy += fruitB.cy
                    neighborCount += 1
        if neighborCount > 0:
            cx /= neighborCount
            cy /= neighborCount
            fruitA.xVelocity += (cx - fruitA.cx) * centeringFactor
            fruitA.yVelocity += (cy - fruitA.cy) * centeringFactor


def seperation(fruits):
    avoidfactor = 0.5
    for fruitA in fruits:
        disX = 0
        disY = 0
        for fruitB in fruits:
            if fruitA != fruitB:
                if distance(fruitA.cx, fruitA.cy, fruitB.cx, fruitB.cy) < fruitA.r+fruitB.r+5:
                    disX += fruitA.cx - fruitB.cx
                    disY += fruitA.cy - fruitB.cy
        fruitA.xVelocity += disX*avoidfactor
        fruitA.yVelocity += disY*avoidfactor

def alignment(fruits):
    matchingFactor = 1.3
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
    turnFactor = 8.5
    for fruit in fruits:
        if fruit.cx <= 400:
            fruit.xVelocity += turnFactor
        elif x-400 <= fruit.cx:
            fruit.xVelocity -= turnFactor
        if fruit.cy <= 400:
            fruit.yVelocity += turnFactor
        elif y-400 <= fruit.cy:
            fruit.yVelocity -= turnFactor