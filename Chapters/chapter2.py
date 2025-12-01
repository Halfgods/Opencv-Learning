# splitting the image into its respective channels
# Best example with the OpenCV logo
import cv2 as cv
import numpy as np # You need numpy for this

img = cv.imread("./Data/opencv-logo-white.png")
img = cv.resize(img, (500, 500))
cv.imshow("Original Image", img)
b, g, r = cv.split(img)

# Create a blank black image of the same shape
zeros = np.zeros(img.shape[:2], dtype="uint8")

# MERGE but keep other channels dead (Zero)
# Order is B, G, R
blue_view = cv.merge([b, zeros, zeros])   # Only Blue has data
green_view = cv.merge([zeros, g, zeros])  # Only Green has data
red_view = cv.merge([zeros, zeros, r])    # Only Red has data

cv.imshow("True Blue Perception", blue_view)
cv.imshow("True Green Perception", green_view)
cv.imshow("True Red Perception", red_view)

cv.waitKey(0)
cv.destroyAllWindows()