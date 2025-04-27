import random
import numpy as np

import turtle


def previewPickFile(objectBuffer,res = 16):
    width = objectBuffer["width"]
    height = objectBuffer["height"]

    colors = [[random.randint(0,255)/255 for y in range(3)] for x in range(5)]
    i = 0
    turtle.tracer(False)
    turtle.penup()
    
    for y in range(height):
        for x in range(width):
            if x%res == 0:
                if y%res == 0:
                    turtle.goto((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE)
                    turtle.color(colors[objectBuffer["data"][i]])
                    turtle.stamp()
            i+=1
    turtle.update()


def viewPngBuffer(pngBuffer,res = 16,doTracer = False,SupressErrors = False):
    width = pngBuffer["width"]
    height = pngBuffer["height"]

    #colors = [[random.randint(0,255)/255 for y in range(3)] for x in range(5)]
    i = 0
    turtle.tracer(doTracer)
    turtle.penup()
    turtle.shapesize((PIXEL_SIZE/SHAPE_SIZE)*res)
    for y in range(height):
        for x in range(width):
            if x%res == 0:
                if y%res == 0:
                    try:
                        if not False in [np.isfinite(pngBuffer["data"][i][x]) for x in range(3)]:
                            turtle.goto((x)*PIXEL_SIZE,-(y)*PIXEL_SIZE)
                            turtle.color([pngBuffer["data"][i][x] for x in range(3)])
                            turtle.stamp()
                    except Exception as e:
                        #print([np.isfinite(pngBuffer["data"][i][x]) for x in range(3)])
                        if not SupressErrors:
                            print(f"Error: {e} - {pngBuffer['data'][i]}")
            i+=1
    turtle.update()


def viewPositionBuffer(pngBuffer,res = 1,d=100,objectBuffer = None):
    width = pngBuffer["width"]
    height = pngBuffer["height"]

    #colors = [[random.randint(0,255)/255 for y in range(3)] for x in range(5)]
    i = 0
    turtle.tracer(False)
    turtle.pendown()
    for y in range(height):
        for x in range(width):
            if x%res == 0:
                if y%res == 0:
                    if objectBuffer != None:
                        print(objectBuffer["data"][i])
                        if objectBuffer["data"][i] == 0:
                            
                            continue
                    pos = [pngBuffer["data"][i][j]*255 for j in range(3)]
                    x,y,z = pos
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
                            turtle.goto(px*PIXEL_SIZE,(py)*PIXEL_SIZE)
                            #turtle.goto((x/res)*PIXEL_SIZE,(y/res)*PIXEL_SIZE)
                            color = [max(0,(pos[i]/255)) for i in range(3)]
                            color = [min(1,color[i]) for i in range(3)]
                            turtle.color(color)
                            #turtle.stamp()
                            
                            turtle.goto((x)*PIXEL_SIZE,(y)*PIXEL_SIZE)
                            turtle.stamp()
            i+=1
        turtle.update()

def clear():
    turtle.clear()
            



SHAPE_SIZE = 20
PIXEL_SIZE = 0.25
turtle.shape("square")
turtle.shapesize(PIXEL_SIZE/SHAPE_SIZE)
#turtle.stamp()
#turtle.goto(10,10)
