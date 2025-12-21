import cv2 as cv
import numpy as np
import imutils 
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the input image")
args = vars(ap.parse_args())
img = cv.imread(args["image"])
gray = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray , (3,3) , 0)
cv.namedWindow("Canny Edges")
cv.resizeWindow("Canny Edges", 640, 240)
cv.createTrackbar("Min Threshold" , "Canny Edges" , 0 , 255 , lambda x: None)
cv.createTrackbar("Max Threshold" , "Canny Edges" , 0 , 255 , lambda x: None)
while True:
    minThresh = cv.getTrackbarPos("Min Threshold" , "Canny Edges")
    maxThresh = cv.getTrackbarPos("Max Threshold" , "Canny Edges")
    edged = cv.Canny(gray , minThresh , maxThresh)
    cv.imshow("Canny Edges" , edged)
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break
print(minThresh , maxThresh)
cv.destroyAllWindows()