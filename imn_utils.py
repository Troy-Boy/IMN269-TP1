import cv2
import numpy as np
import PIL
 
# Picture path
img = cv2.imread('images/Koala_climbing_tree.jpg')
coordoX = []
coordoY = []

 
def getCoordonnee(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        xy = "%d,%d" % (x, y)
        coordoX.append(x)
        coordoY.append(y)
        if(len(coordoX)%2 == 0):
            print("should draw line")
            cv2.line(img, (x,y),
            (coordoX[len(coordoX)-2],coordoY[len(coordoX)-2]),
            (0,0,0), thickness=3)
            print(x,y)
            print(coordoX[len(coordoX)-1],coordoY[len(coordoX)-1])
        cv2.circle(img, (x, y), 1, (200, 200, 200), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("fenetre image", img)
        #print(x,y)
 


 
cv2.namedWindow("fenetre image")
cv2.setMouseCallback("fenetre image", getCoordonnee)
cv2.imshow("fenetre image", img)
cv2.waitKey(0)
print(coordoX[0], coordoY[0])
 