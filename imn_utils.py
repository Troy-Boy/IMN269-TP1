import cv2
import numpy as np
import PIL
import balls

# POUR INSTALLER cv2
# pip install opencv-python

# Picture path
img = cv2.imread('images/building.jpg')
coordoX =[]# [556, 759, 563, 763, 553, 226, 414, 346]
coordoY =[]# [746, 687, 535, 582, 747, 721, 255, 273]
halfX = len(img[0])
halfY = len(img)
# horizon = [0, 0, 0]


def update(event, x, y, flags, param):
    
    if (event == cv2.EVENT_LBUTTONDOWN):
        xy = "%d,%d" % (x, y)
        coordoX.append(x)
        coordoY.append(y)
        print(x, y)

    for i in coordoX:
        if(i % 2 != 0):

            cv2.line(img, (coordoX[i], coordoY[i]),
                     (coordoX[i+1], coordoY[i+1]),
                     (0, 0, 0), thickness=3)

        cv2.circle(img, (coordoX[i],  coordoY[i]),
                   1, (200, 200, 200), thickness=-1)
        cv2.putText(img, (coordoX[i],  coordoY[i]), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)

    cv2.imshow("fenetre image", img)

    if (len(coordoX) == 8 and len(coordoY) == 8):
        f1 = calculIntersection(0)  # marche pas mais bon who cares amarite
        f2 = calculIntersection(4)
        horizon = calculateHorizon(f1, f2)
        print("thats horizon:")
        print(horizon)
        matH = calculateH(horizon)
        print(matH.dot(horizon))
        imgTransfo = cv2.warpPerspective(img, matH, (len(img[0]), len(
            img)))

        cv2.imshow("Resultat", imgTransfo)


def calculateH(df):
    h2 = np.zeros((3, 3), dtype=np.float64)
    h2[0, 0] = 1
    h2[1, 1] = 1
    h2[2, :] = df
    print("hold the line, TA TA TA TA, love isn't always on time\n")
    print(h2)
    return h2


def calculateHorizon(f1, f2):
    # pFuite1 = balls.seg_intersect(coordoX[0]-coordoX[1], coordoY[0] - coordoY[1],
    #                               coordoX[2]-coordoX[3], coordoY[2] - coordoY[3])
    # pFuite2 = balls.seg_intersect(coordoX[4]-coordoX[5], coordoY[4] - coordoY[5],
    #                               coordoX[6]-coordoX[7], coordoY[6] - coordoY[7])
    # return np.matmul(pFuite1, pFuite2)

    print("thats f1:")
    print(f1)
    print("thats f2:")
    print(f2)

    d_horizon = np.cross(f1, f2)

    return d_horizon


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
cv2.setMouseCallback("fenetre image", update)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)

# print(coordoX[0], coordoY[0])
