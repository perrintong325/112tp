# from fruitMovement import distance

#reference: stanford cs notes and vergnet boids seudocode
def boids(fruits,x,y):
    rule1(fruits)
    rule2(fruits)
    #rule3(fruits)
    for fruit in fruits:
        fruit.cx += fruit.xVelocity
        fruit.cy += fruit.yVelocity
    bound(fruits,x,y)
    return fruits

# reference: cs academy


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def rule1(fruits):
    cx = 0
    cy = 0
    for fruit in fruits:
        cx += fruit.cx
        cy += fruit.cy
    for fruit in fruits:
        fruit.perceivedCx = (cx-fruit.cx)/(len(fruits)-1)
        fruit.perceivedCy = (cy-fruit.cy)/(len(fruits)-1)
        fruit.cx += (fruit.perceivedCx - fruit.cx)/100
        fruit.cy += (fruit.perceivedCy - fruit.cy)/100

def rule2(fruits):
    for fruitA in fruits:
        disX = 0
        disY = 0
        for fruitB in fruits:
            if fruitA != fruitB:
                if distance(fruitA.cx, fruitA.cy, fruitB.cx, fruitB.cy) < fruitA.r+fruitB.r + 20:
                    disX = disX - (fruitB.cx - fruitA.cx)
                    disY = disY - (fruitB.cy - fruitA.cy)
        fruitA.cx -= disX
        fruitA.cy -= disY

def rule3(fruits):
    vx = 0
    vy = 0
    for fruit in fruits:
        vx += fruit.xVelocity
        vy += fruit.yVelocity
    for fruit in fruits:
        fruit.perceivedVx = (vx-fruit.xVelocity)/(len(fruits)-1)
        fruit.perceivedVy = (vy-fruit.yVelocity)/(len(fruits)-1)
        fruit.xVelocity += (fruit.perceivedVx - fruit.xVelocity)/8
        fruit.yVelocity += (fruit.perceivedVy - fruit.yVelocity)/8

def bound(fruits,x,y):
    for fruit in fruits:
        if fruit.cx <= 15:
            fruit.cx += 30
            fruit.xVelocity = -fruit.xVelocity
        elif x-15 <= fruit.cx:
            fruit.cx -= 30
            fruit.xVelocity = -fruit.xVelocity
        if fruit.cy <= 15:
            fruit.cy += 30
            fruit.yVelocity = -fruit.yVelocity
        elif y-15 <= fruit.cy:
            fruit.cy -= 30
            fruit.yVelocity = -fruit.yVelocity