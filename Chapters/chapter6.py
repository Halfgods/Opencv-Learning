# Lets do Shape Detection now!
import cv2 as cv
import numpy as np
from chapter3 import stackImages # Importing the stackImages function from chapter3
img = cv.imread("./Data/shapes.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (11,11), 1)
thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C , cv.THRESH_BINARY_INV, 11, 2)
canny = cv.Canny(blur, 50, 125)
blank = np.zeros_like(img)
contourimg = img.copy()
def getContours(img):
    contours , hierarchy = cv.findContours(img , cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        print(area)
        if area>500:
            cv.drawContours(contourimg , cnt , -1 , (255,0,0), 3)
            perimeter = cv.arcLength(cnt , True)
            print(perimeter , "perimeter")
            approx = cv.approxPolyDP(cnt , 0.02*perimeter , True)
            print(len(approx) , "approx len")
            objCor = len(approx)
            x , y , w , h = cv.boundingRect(approx)
            centerX = x + (w // 2)
            centerY = y + (h // 2)
            if objCor == 3:
                objectType = "Triangle"
                cv.putText(contourimg , objectType , (centerX , centerY) , cv.FONT_HERSHEY_COMPLEX , 0.5 , (0,0,0) ,2)
            elif objCor == 4:
                cv.putText(contourimg , "Square" , (centerX , centerY) , cv.FONT_HERSHEY_COMPLEX , 0.5 , (0,0,0) ,2)
            else:
                cv.putText(contourimg , "Polygon" , (centerX , centerY) , cv.FONT_HERSHEY_COMPLEX , 0.5 , (0,0,0) ,2)
            cv.rectangle(contourimg,(x,y),(x+w , y+h) , (0,255,0) ,2)
            
        else:
            continue
getContours(canny) # Just run it. Don't assign it.
stack = stackImages(0.6, ([img,contourimg]))
cv.imshow("Stack", stack)
cv.waitKey(0)
cv.destroyAllWindows()