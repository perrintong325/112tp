from cmu_cs3_graphics import *
import math
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def angleCalc(p1,p2):
    dx = p2[0]-p1[0]
    dy = p1[1] - p2[1]
    if dy != 0:
        angle = math.atan(dx/dy)* 360/ (2*math.pi)
    else:
        angle = 90
    return angle

def onAppStart(app):
    app.cx=528
    app.cy=473
    app.p1= (472.6177066027883, 449.91750494281143)
    app.p2= (566.9486769466083, 427.3600989910284)
    app.Awidth = abs(distance(app.p1[0],app.p1[1],app.p2[0],app.p2[1]))
    app.Aheight = 24.670014609684653*2
    app.sweepAngle=180
    app.color = 'red'

def redrawAll(app):
    
    drawArc(app.cx+100, app.cy, app.Awidth,app.Aheight, 270,app.sweepAngle, fill=app.color)
    print(app.Aheight+(120-(app.Aheight/2))*2)
    sweep = 360-abs(angleCalc(app.p1, (app.cx, app.cy)))-abs(angleCalc(app.p2, (app.cx, app.cy)))
    drawArc(app.cx, app.cy, 120,120, 270,bottomSweep, fill=app.color)
    drawPolygon(app.p1[0],app.p1[1],app.p2[0],app.p2[1],app.cx,app.cy, fill=app.color)
runApp(width=1280, height=720)