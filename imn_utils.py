import cv2
import numpy as np
import PIL
from numpy.lib.shape_base import _make_along_axis_idx
import balls
from PIL import Image

# POUR INSTALLER cv2
# pip install opencv-python

# Picture path
img = cv2.imread('images/building.jpg')
coordoX =[325,1040,325,1045,325,103,325,100]#[261,444,138,564]#eglise [556, 759, 563, 763, 553, 226, 414, 346]
coordoY =[27,441,924,886,29,471,926,894]#[379,373,621,614]#eglise [746, 687, 535, 582, 747, 721, 255, 273]
# horizon = [0, 0, 0]


def update(event, x, y, flags, param):
    # if event == cv2.EVENT_LBUTTONDOWN:
    #     xy = "%d,%d" % (x, y)
    #     coordoX.append(x)
    #     coordoY.append(y)
    #     cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
    #     cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
    #                 1.0, (0, 0, 0), thickness=1)
    #     cv2.imshow("fenetre image", img)
    #     print(x,y)
    if (event == cv2.EVENT_LBUTTONDOWN):
    #     xy = "%d,%d" % (x, y)
    #     coordoX.append(x)
    #     coordoY.append(y)
    #     print(x, y)
    #     cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
    #     cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
    #                 1.0, (0, 0, 0), thickness=1)
    #     cv2.imshow("fenetre image", img)

        if(len(coordoX) % 2 == 0):
            cv2.line(img, (coordoX[len(coordoX)-1], coordoY[len(coordoX)-1]),
                    (coordoX[len(coordoX)-2], coordoY[len(coordoX)-2]),
                    (0, 0, 0), thickness=3)

        cv2.imshow("fenetre image", img)

        if (len(coordoX) == 8 and len(coordoY) == 8):
            printCoordo()
            if(len(coordoX) % 2 == 0):
                cv2.line(img, (coordoX[len(coordoX)-1], coordoY[len(coordoX)-1]),
                (coordoX[len(coordoX)-2], coordoY[len(coordoX)-2]),
                (0, 0, 0), thickness=3)
            f1 = calculIntersection(0)  # marche pas mais bon who cares amarite
            f2 = calculIntersection(4)
            horizon = np.cross(f1, f2)
            print("thats horizon:")
            print(horizon)
            matH = calculateH(horizon)
            print(matH.dot(horizon))
            imgTransfo = np.zeros_like(img)
            imgTransfo = warpPerspFuckingShit(img, matH)
            print("sohuld print")
            cv2.imshow("Resultat", imgTransfo)

def warpPerspFuckingShit(img, H):
    sizeX = len(img)
    sizeY = len(img[0])
    print(H)
    maxX=0
    maxY=0
    minX=999999999
    minY=999999999
    for y in range(0, sizeY-1):
        for x in range(0, sizeX-1):
            posInit = np.array([x,y,1])
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
    imgRes = np.zeros((newSizeX+1,newsizeY+1,3))
    for y in range(0, sizeY-1):
        for x in range(0, sizeX-1):
            posInit = np.array([x,y,1])
            posRes = posInit.dot(H)
            resX = int(posRes[0])
            resY = int(posRes[1])
            imgRes[resX-minX,resY-minY] = img[x,y]
    imgFinal = cv2.resize(imgRes, (sizeX,sizeY), interpolation = cv2.INTER_AREA)
    print("max X : ", maxX)
    print("min X : ", minX)
    print("max Y : ", maxY)
    print("min Y : ", minY)

    return imgFinal

def calculateH(df):
    h2 = np.identity(3, dtype = float)
    h2[2, :] = df
    print("hold the line, TA TA TA TA, love isn't always on time\n")
    print(h2)
    return h2

def printCoordo():
    for i in range (0,7):
        cv2.circle(img, (coordoX[i], coordoY[i]), 1, (0, 0, 255), thickness=-1)
        cv2.imshow("fenetre image", img)

def calculIntersection(index):
    x1 = coordoX[index] /100
    y1 = coordoY[index] /100
    p1 = [x1, y1, 1]

    print("thats p1:", p1)

    x2 = coordoX[index+1] /100
    y2 = coordoY[index+1] /100
    p2 = [x2, y2, 1]

    print("thats p2:", p2)

    d1 = np.cross(p1, p2)

    print("thats d1:", d1)

    x3 = coordoX[index+2] /100
    y3 = coordoY[index+2] /100
    p3 = [x3, y3, 1]

    print("thats p3:", p3)

    x4 = coordoX[index+3] /100
    y4 = coordoY[index+3] /100
    p4 = [x4, y4, 1]

    print("thats p4:", p4)

    d2 = np.cross(p3, p4)
    print("thats d2:", d2)

    f = np.cross(d1, d2)
    print("thats f:", f)

    return f


cv2.namedWindow("fenetre image")
cv2.moveWindow("fenetre image", 70, 30)
cv2.setMouseCallback("fenetre image", update)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)

# print(coordoX[0], coordoY[0])
