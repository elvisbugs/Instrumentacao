import numpy as np
import cv2 as cv

def radToDegree(rad):
    x = rad * 180/np.pi
    return x

def degreeToRad(degree):
    x = degree * np.pi/180
    return x

def positionInPoint(degree):
    xy = []
    rad = degreeToRad(degree)
    x = np.cos(rad)
    y = np.sin(rad)
    xy.append(x)
    xy.append(y)
    return xy

def drawHalfCircle(img):
    radium = len(img[0])//2
    yVector = np.zeros([720],dtype=np.uint8)
    for i in range(0,720):
        point = positionInPoint((180/720)*(i))
        x = int(point[0] * radium) + 359
        y = int(point[1] * radium)
        img[y,x,0] = 0
        img[y,x,1] = 0
        img[y,x,2] = 0
        yVector[x] = y
    
    for i in range(len(img)):
        for j in range(len(img[i])):
                for k in range(len(img[i,j])):
                    img[i,j,k] = 0

    return img

def rotate180degree(img):
    imgNew = img.copy()
    x = 0
    for i in range(len(img)-1,0,-1):
        y = 0
        for j in range(len(img[i])-1,0,-1):
            imgNew[x,y] = img[i,j]
            y+=1
        x += 1
    return imgNew

img = np.zeros([411,720,3],dtype=np.uint8)
img.fill(255)

img = drawHalfCircle(img)

cv.imshow("Sample",rotate180degree(img))

cv.waitKey(0)