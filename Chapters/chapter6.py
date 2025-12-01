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
        cv.drawContours(contourimg , cnt , -1 , (255,0,0), 3)
        
getContours(canny) # Just run it. Don't assign it.
stack = stackImages(0.5, ([img, gray,thresh],[blur, contourimg,canny]))
cv.imshow("Stack", stack)
cv.waitKey(0)
cv.destroyAllWindows()