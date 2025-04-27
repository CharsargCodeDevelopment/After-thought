import random
import matplotlib.pyplot as plt
import numpy as np
 

global _3DPointBuffer
_3DPointBuffer = {"x":[],"y":[],"z":[],"c":[]}

def Draw2dPoint(x,y,color):
    pass
def Draw3dPoint(x,y,z,color):
    global _3DPointBuffer
    _3DPointBuffer["x"].append(x)
    _3DPointBuffer["y"].append(y)
    _3DPointBuffer["z"].append(z)
    _3DPointBuffer["c"].append(color)
    
def previewPickFile(objectBuffer,res = 16):
    width = objectBuffer["width"]
    height = objectBuffer["height"]

    colors = [[random.randint(0,255)/255 for y in range(3)] for x in range(5)]
    i = 0
    #turtle.tracer(False)
    #turtle.penup()
    for y in range(height):
        for x in range(width):
            if x%res == 0:
                if y%res == 0:
                    Draw2dPoint((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE,colors[objectBuffer["data"][i]])
                    #turtle.goto((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE)
                    #turtle.color(colors[objectBuffer["data"][i]])
                    #turtle.stamp()
            i+=1
    #turtle.update()


def viewPngBuffer(pngBuffer,res = 16):
    width = pngBuffer["width"]
    height = pngBuffer["height"]

    #colors = [[random.randint(0,255)/255 for y in range(3)] for x in range(5)]
    i = 0
    #turtle.tracer(False)
    #turtle.penup()
    for y in range(height):
        for x in range(width):
            if x%res == 0:
                if y%res == 0:
                    #turtle.goto((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE)
                    #turtle.color([pngBuffer["data"][i][x] for x in range(3)])
                    Draw2dPoint((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE,[pngBuffer["data"][i][x] for x in range(3)])
                    #turtle.stamp()
            i+=1
   # turtle.update()


def viewPositionBuffer(pngBuffer,res = 16,objectBuffer = None):
    width = pngBuffer["width"]
    height = pngBuffer["height"]

    #colors = [[random.randint(0,255)/255 for y in range(3)] for x in range(5)]
    i = 0
    #turtle.tracer(False)
    #turtle.pendown()
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for y in range(height):
        for x in range(width):
            if x%res == 0:
                if y%res == 0:
                    #print(pos)
                    pos = [pngBuffer["data"][i][j]*255 for j in range(3)]
                    color = [max(0,(pos[j]/255)) for j in range(3)]
                    color = [min(1,color[j]) for j in range(3)]
                    x1,y1,z1 = pos
                    Draw3dPoint(x1,y1,z1,color)
                    """
                    
                    if pos != [0,0,0]:
                        pass
                        if pos != [170.0, 170.0, 170.0]:
                            pass
                            #print(pos)
                    if z != 0:
                        if pos != [170.0, 170.0, 170.0]:
                            px = (x/y)*d
                            py = (z/y)*d
                            px = x
                            py = y
                            #turtle.goto(px*PIXEL_SIZE,(py)*PIXEL_SIZE)
                            #turtle.goto((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE)
                            color = [max(0,(pos[i]/255)) for i in range(3)]
                            color = [min(1,color[i]) for i in range(3)]
                            #turtle.color(color)
                            #turtle.stamp()
                            
                            #turtle.goto((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE)
                            #turtle.stamp()
                    """
            i+=1
    global _3DPointBuffer
    ax.scatter(_3DPointBuffer["x"], _3DPointBuffer["y"], _3DPointBuffer["z"], c = _3DPointBuffer["c"])
    #print(_3DPointBuffer)
    plt.show()
       # turtle.update()
            
            

def SetShapeSize(size):
    pass

SHAPE_SIZE = 20
PIXEL_SIZE = 2
#turtle.shape("square")
SetShapeSize(PIXEL_SIZE/SHAPE_SIZE)
#turtle.stamp()
#turtle.goto(10,10)
