import cv2
import numpy as np
import PIL
import balls

# POUR INSTALLER cv2
# pip install opencv-python

# Picture path
img = cv2.imread('images/Koala_climbing_tree.jpg')
coordoX = []
coordoY = []


def update(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        xy = "%d,%d" % (x, y)
        coordoX.append(x)
        coordoY.append(y)
        if(len(coordoX) % 2 == 0):
            print("should draw line")
            cv2.line(img, (x, y),
                     (coordoX[len(coordoX)-2], coordoY[len(coordoX)-2]),
                     (0, 0, 0), thickness=3)
            print(x, y)
            print(coordoX[len(coordoX)-1], coordoY[len(coordoX)-1])
        cv2.circle(img, (x, y), 1, (200, 200, 200), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("fenetre image", img)
    if (len(coordoX) == 8):
        print(calculateHorizon())  # marche pas mais bon who cares amarite


# ok sa marche pas rip
def calculateHorizon():
    # pFuite1 = balls.seg_intersect(coordoX[0]-coordoX[1], coordoY[0] - coordoY[1],
    #                               coordoX[2]-coordoX[3], coordoY[2] - coordoY[3])
    # pFuite2 = balls.seg_intersect(coordoX[4]-coordoX[5], coordoY[4] - coordoY[5],
    #                               coordoX[6]-coordoX[7], coordoY[6] - coordoY[7])
    # return np.matmul(pFuite1, pFuite2)

    
    v = 1
    return v


cv2.namedWindow("fenetre image")
cv2.setMouseCallback("fenetre image", update)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)
print(coordoX[0], coordoY[0])
