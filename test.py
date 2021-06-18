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
coordo = [(3.17, 2.78, 1), (4.21, 2.12, 1), (2.14, 2.11, 1), (3.17, 1.81, 1),
          (3.18, 2.79, 1), (2.13, 2.12, 1), (4.21, 2.12, 1), (3.18, 1.81, 1)]
VP = [(0.33, 1.0, 1), (0.6, 1.0, 1)]


def update(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
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
            # calcul des points d'intersection
            vp1 = calculIntersection(0)
            vp2 = calculIntersection(4)
            realVp1 = abs(vp1*100/vp1[2])
            realVp2 = abs(vp2*100/vp2[2])
            print("VPs:", vp1, vp2)
            p1 = [int(realVp1[0]), int(realVp1[1])]
            p2 = [int(realVp2[0]), int(realVp2[1])]

            # affichage des points et horizon
            print(p1, p2)
            cv2.circle(img, p1, 2, (255, 0, 0), thickness=2)
            cv2.imshow("fenetre image", img)
            cv2.circle(img, p2, 2, (255, 0, 0), thickness=2)
            cv2.imshow("fenetre image", img)
            cv2.line(img, [20, 99], [620, 99], (86, 137, 200), thickness=2)
            cv2.line(img, p1, p2, (255, 0, 0), thickness=1)

            cv2.imshow("fenetre image", img)

            # Calcul de l'horizon
            # horizon = np.cross([0.33, 1, 1], [6, 1, 1])
            horizon = np.cross(abs(vp1), (vp2))

            # print("horizon:", horizon)
            horizon[0] = 0
            # print("horizon:", horizon)

            realHorizon = abs(horizon*100/horizon[2])
            # print("real horizon", realHorizon)

            # calcul de H2
            h2 = calculateH(horizon)
            # print("H:", h2)

            # x = np.matmul(h2, vp2)

            # print("X", x)
            # h22 = np.linalg.inv(h2)
            # y = h22.transpose()
            # t = np.matmul(y, horizon)
            # print("T", t)

            # unwarp
            newImg = unwarpImage(h2)
            # cv2.imshow("res", newImg)
            cv2.imwrite("res.jpg", newImg)
            print("fini")


def unwarpImage(h2):
    newImg = np.zeros_like(img)
    imW = len(img[0])
    imH = len(img)
    print(imH, imW)
    maxX = 0
    minX = 0
    maxY = 0
    minY = 0
    h2 = abs(h2)
    # print(newImg, len(newImg), len(newImg[0]))
    # print(len(img), len(img[370][630]))
    for i in range(0, imW-1):
        for j in range(0, imH-1):
            pointToTransform = [i/imW, j/imH, 1]
            transf = np.matmul(h2, pointToTransform)
            # print(pointToTransform)
            transf = transf/transf[2]
            # if(i % 20 == 0):
            # print("transfo", transf)
            newX = int(transf[0]*631)
            newY = int(transf[1]*370)
            if(newX >= maxX):
                maxX = newX
            else:
                if(newX <= minX):
                    minX = newX
            if(newY >= maxY):
                maxY = newY
            else:
                if(newY <= minY):
                    minY = newY

            # print("new x:", newX, "new y:", newY)
            # print("i:", i, "j:", j)

            if(newX < 631 and newY < 370):
                t = img[j][i]
                newImg[newY][newX] = t
            # else:
            #     print("out of bounds")

    print(maxX, maxY, minX, minY)
    return newImg


def calculateH(df):
    h2 = np.identity(3, dtype=float)
    h2[2, :] = df
    print("hold the line, TA TA TA TA, love isn't always on time\n")
    print(h2)
    return h2


def calculIntersection(index):
    print(coordo)
    d1 = np.cross(coordo[index], coordo[index+1])
    d2 = np.cross(coordo[index+2], coordo[index+3])
    print("d1:", d1)
    print("d2:", d2)

    vp = np.cross(d1, d2)
    print("VP:", vp)
    return vp


cv2.namedWindow("fenetre image")
cv2.moveWindow("fenetre image", 70, 30)
cv2.setMouseCallback("fenetre image", update)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)
