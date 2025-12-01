# Chapter 1: Introduction to OpenCV
import cv2 as cv
import numpy as np
# Load an image from file
# You can add a second arg to imread to specify how to read the image
"""cv2.IMREAD_UNCHANGED  or -1
cv2.IMREAD_GRAYSCALE  or 0
cv2.IMREAD_COLOR  or 1"""

imgcolor = cv.imread("./Data/opencv-logo.png" , 1)
imggray = cv.imread("./Data/opencv-logo.png" , 0)
imgunchanged = cv.imread("./Data/opencv-logo.png" , -1)
black = np.zeros(imgcolor.shape[:2] , dtype = "uint8")   # Create a black image of the same height and width

cv.imshow("Black Image", black)  # Show the black image
cv.imshow("Unchanged Image", imgunchanged) # Show the unchanged image
cv.imshow("Gray Image", imggray) # Show the Gray image
cv.imshow("color Image", imgcolor) # Show the Color image
cv.imwrite("./Data/opencv-logo-gray.png" , imggray) # Write the gray image to a file
cv.waitKey(0) # Wait for a key press to close the windows or wait infinitely
cv.destroyAllWindows()
