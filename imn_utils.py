import cv2
import numpy as np
import PIL
import balls

# POUR INSTALLER cv2
# pip install opencv-python

# Picture path
img = cv2.imread('images/church.jpg')
coordoX = []
coordoY = []
f1 = []
f2 = []
horizon = []


def update(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        xy = "%d,%d" % (x, y)
        coordoX.append(x)
        coordoY.append(y)
        print(x, y)

        if(len(coordoX) % 2 == 0):
            print("should draw line")
            cv2.line(img, (x, y),
                     (coordoX[len(coordoX)-2], coordoY[len(coordoX)-2]),
                     (0, 0, 0), thickness=3)
        cv2.circle(img, (x, y), 1, (200, 200, 200), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("fenetre image", img)

    if (len(coordoX) == 8 and len(coordoY) == 8):
        f1 = calculIntersection(0)  # marche pas mais bon who cares amarite
        f2 = calculIntersection(4)
        horizon = calculateHorizon()
        print(horizon)
        cv2.line(img, (horizon[0] * 100, horizon[1] * 100), (horizon[0] * 100 + 100, horizon[1] * 100 + 100)
                 (255, 0, 0), thickness=3)
        cv2.imshow("fenetre image", img)


def calculateHorizon():
    # pFuite1 = balls.seg_intersect(coordoX[0]-coordoX[1], coordoY[0] - coordoY[1],
    #                               coordoX[2]-coordoX[3], coordoY[2] - coordoY[3])
    # pFuite2 = balls.seg_intersect(coordoX[4]-coordoX[5], coordoY[4] - coordoY[5],
    #                               coordoX[6]-coordoX[7], coordoY[6] - coordoY[7])
    # return np.matmul(pFuite1, pFuite2)

    d_horizon = np.cross(f1, f2)

    print(f1)
    print(f2)
    return d_horizon


def calculIntersection(index):
    x1 = coordoX[index] / 100
    y1 = coordoY[index] / 100
    p1 = [x1, y1, 1]

    x2 = coordoX[index+1] / 100
    y2 = coordoY[index+1] / 100
    p2 = [x2, y2, 1]

    d1 = np.cross(p1, p2)

    x3 = coordoX[index+2] / 100
    y3 = coordoY[index+2] / 100
    p3 = [x3, y3, 1]

    x4 = coordoX[index+3] / 100
    y4 = coordoY[index+3] / 100
    p4 = [x4, y4, 1]

    d2 = np.cross(p3, p4)

    f = np.cross(d1, d2)

    return f


cv2.namedWindow("fenetre image")
cv2.setMouseCallback("fenetre image", update)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)
# print(coordoX[0], coordoY[0])
