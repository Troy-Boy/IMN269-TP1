from typing import final
import cv2
import numpy as np
import PIL
from numpy.lib.shape_base import _make_along_axis_idx
import balls
from PIL import Image

# POUR INSTALLER cv2
# pip install opencv-python

# Picture path
img = cv2.imread('images/PERSPECTIVE05.jpg')
# [261,444,138,564]#eglise [556, 759, 563, 763, 553, 226, 414, 346]
# coordoX = [325, 1040, 325, 1045, 325, 103, 325, 100]
# [379,373,621,614]#eglise [746, 687, 535, 582, 747, 721, 255, 273]
# coordoY = [27, 441, 924, 886, 29, 471, 926, 894]
coordoX = []
coordoY = []
coordo = np.array([(3.17,1.81,1), (4.21,2.11,1), (2.14,2.13,1), (3.17,2.78,1), 
                    (4.21,2.11,1), (3.17,2.78,1),(3.17,1.81,1),(2.14,2.13,1)])
VP = [(0.33, 1.0, 1), (0.6, 1.0, 1)]
# vp1 = (0, 0, 0)
# vp2 = (0, 0, 0)
# horizon = [0, 0, 0]


def computeThings():
    # if event == cv2.EVENT_LBUTTONDOWN:
    #     xy = "%d,%d" % (x, y)
    #     coordoX.append(x)
    #     coordoY.append(y)
    #     cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
    #     cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
    #                 1.0, (0, 0, 0), thickness=1)
    #     cv2.imshow("fenetre image", img)
    #     print(x,y)

    if (3>1):
        # xy = "%d,%d" % (x, y)
        # print(x, y)
        # if(len(coordo) <= 4):
        #     cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=1)
        #     cv2.imshow("fenetre image", img)
        # if(len(coordo) > 4):
        #     cv2.circle(img, (x, y), 1, (0, 255, 0), thickness=1)
        #     cv2.imshow("fenetre image", img)

        # coordo.append((x/100, y/100, 1))
        if(len(coordo) == 8):
            vp1 = calculIntersection(0)
            vp2 = calculIntersection(4)
            p1 = [int(vp1[0]), int(vp1[1])]
            p2 = [int(vp2[0]), int(vp2[1])]

            print(p1, p2)
            cv2.circle(img, p1, 2, (255, 0, 0), thickness=2)
            cv2.imshow("fenetre image", img)
            cv2.circle(img, p2, 2, (255, 0, 0), thickness=2)
            cv2.imshow("fenetre image", img)

            sizeX = len(img)
            sizeY = len(img[0])
            minX = 999999999999
            minY = 999999999999
            maxX = -999999999999
            maxY = -999999999999
            matH = calculateH(np.cross(vp1/100, vp2/100))
            newCoordo = np.array(coordo)
            for i in range (0,8):
                temp = np.array([coordo[i]])
                temp = coordo[i]*100
                newCoordo[i] = temp.dot(matH)
                if newCoordo[(i,0)] < minX:
                    minX = newCoordo[(i,0)]
                if newCoordo[(i,0)] > maxX:
                    maxX = newCoordo[(i,0)]
                if newCoordo[(i,1)] < minY:
                    minY = newCoordo[(i,1)]
                if newCoordo[(i,1)] > maxY:
                    maxY = newCoordo[(i,1)]
            print("max X : ", maxX)
            print("min X : ", minX)
            print("max Y : ", maxY)
            print("min Y : ", minY)
            finalCoordo = np.array  (coordo)
            for i in range(0,4):
                x1 = int((newCoordo[(i*2,0)]-minX)*sizeX*2/maxX)
                y1 = int((newCoordo[(i*2,1)]-minY)*sizeY*2/maxY)
                x2 = int((newCoordo[((i*2)+1,0)]-minX)*sizeX*2/maxX)
                y2 = int((newCoordo[((i*2)+1,1)]-minY)*sizeY*2/maxY)

                print(x1,y1)
                print(x2,y2)
                cv2.line(img, (x1,y1), 
                (x2,y2),(0, 0, 0), thickness=3)
            cv2.imshow("fenetre image", img)



            

            


def warpPerspFuckingShit(img, H):
    sizeX = len(img)
    sizeY = len(img[0])
    print(H)
    maxX = 0
    maxY = 0
    minX = 999999999
    minY = 999999999
    for y in range(0, sizeY):
        for x in range(0, sizeX):
            posInit = np.array([x, y, 1])
            posRes = posInit.dot(H)
            resX = int(posRes[0])
            resY = int(posRes[1])
            # if(xRes!=0):
            #     print("res x : ", xRes)
            # if(xRes!=0):
            #     print("res y : ", yRes)
            if resX < minX:
                minX = resX
            if resX > maxX:
                maxX = resX
            if resY < minY:
                minY = resY
            if resY > maxY:
                maxY = resY
    newSizeX = maxX - minX
    newsizeY = maxY - minY
    imgRes = np.zeros((newSizeX+1, newsizeY+1, 3))
    for y in range(0, sizeY):
        for x in range(0, sizeX):
            posInit = np.array([x, y, 1])
            posRes = posInit.dot(H)
            resX = int(posRes[0])
            resY = int(posRes[1])
            imgRes[resX-minX, resY-minY] = img[x, y]
    imgFinal = cv2.resize(imgRes, (sizeX, sizeY), interpolation=cv2.INTER_AREA)
    print("max X : ", maxX)
    print("min X : ", minX)
    print("max Y : ", maxY)
    print("min Y : ", minY)

    return imgFinal


def calculateH(df):
    h2 = np.identity(3, dtype=float)
    h2[2, :] = df
    print("hold the line, TA TA TA TA, love isn't always on time\n")
    print(h2)
    return h2


def printCoordo():
    for i in range(0, 8):
        cv2.circle(img, (coordoX[i], coordoY[i]), 1, (0, 0, 255), thickness=-1)
        cv2.imshow("fenetre image", img)


def calculIntersection(index):
    print(coordo)
    d1 = np.cross(coordo[index], coordo[index+1])
    d2 = np.cross(coordo[index+2], coordo[index+3])
    vp = np.cross(d1, d2)
    vp = abs(vp*100/vp[2])

    print("VP:", vp)
    return vp

    # d3 = np.cross(coordo[index], coordo[index+1])
    # d4 = np.cross(coordo[index+2], coordo[index+])
    # vp2 = np.cross(d3, d4)
    # vp2 = abs(vp2*100/vp2[2])
    # print("vp2:", vp2)

def doNothing(event, x, y, flags, param):
    a = 1

cv2.namedWindow("fenetre image")
cv2.moveWindow("fenetre image", 70, 30)
cv2.setMouseCallback("fenetre image", doNothing)
computeThings()
cv2.imshow("fenetre image", img)
cv2.waitKey(0)

# print(coordoX[0], coordoY[0])
