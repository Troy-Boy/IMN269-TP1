import cv2
import numpy as np

# POUR INSTALLER cv2
# pip install opencv-python

# Picture path
img = cv2.imread('images/church.jpg')
height = len(img)
width = len(img[0])

coordo = []


def update(event, x, y, flags, param):

    # select parallel lines
    if (event == cv2.EVENT_LBUTTONDOWN):
        xy = "%d,%d" % (x, y)

        if(len(coordo) <= 4):
            cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=1)
            cv2.imshow("fenetre image", img)
        if(len(coordo) > 4):
            cv2.circle(img, (x, y), 1, (0, 255, 0), thickness=1)
            cv2.imshow("fenetre image", img)

        coordo.append((x/100, y/100, 1))

    if(len(coordo) == 8):
        # calcul des points d'intersection
        vp1 = calculIntersection(0)
        vp2 = calculIntersection(4)

        # ajout des points de fuite
        realVp1 = vp1*100/vp1[2]
        realVp2 = vp2*100/vp2[2]
        p1 = [int(realVp1[0]), int(realVp1[1])]
        p2 = [int(realVp2[0]), int(realVp2[1])]

        # affichage des points et horizon
        cv2.circle(img, p1, 2, (255, 0, 0), thickness=2)
        cv2.imshow("fenetre image", img)
        cv2.circle(img, p2, 2, (255, 0, 0), thickness=2)
        cv2.imshow("fenetre image", img)

        # trace une ligne a l'horizon
        cv2.line(img, p1, p2, (0, 0, 255), thickness=2)

        cv2.imshow("fenetre image", img)

        # Calcul de l'horizon
        horizon = np.cross(vp1, vp2)

        # calcul de H2
        h2 = calculateH(horizon)

        # unwarp
        newImg = unwarpImage(h2)
        cv2.imwrite("images/res.jpg", newImg)
        cv2.imwrite("images/resultat_horizon.jpg", img)


def unwarpImage(h2):
    newImg = np.zeros_like(img)
    imW = len(img[0])
    imH = len(img)
    for i in range(0, imW-1):
        for j in range(0, imH-1):
            # normalise les points
            pointToTransform = [i/(imW), j/(imH), 1]
            transf = np.matmul(h2, pointToTransform)
            transf = transf/transf[2]

            newX = int(transf[0]*imW*30)
            newY = int(transf[1]*imH*30)

            if(newX < imW-1 and newY < imH-1):
                t = img[j][i]
                newImg[newY][newX] = t

    return newImg


def calculateH(df):
    h2 = np.identity(3, dtype=float)
    h2[2, :] = abs(df)
    return h2


def calculIntersection(index):
    d1 = np.cross(coordo[index], coordo[index+1])
    d2 = np.cross(coordo[index+2], coordo[index+3])
    vp = np.cross(d1, d2)
    return vp


cv2.namedWindow("fenetre image")
cv2.moveWindow("fenetre image", 70, 30)
cv2.setMouseCallback("fenetre image", update)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)
