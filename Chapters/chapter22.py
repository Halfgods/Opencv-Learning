import cv2 as cv
import numpy as np
import argparse
import imutils

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="Path to the input image")
# args = vars(ap.parse_args())


img = cv.imread("./Data/tablets.png")
try:
    for angle in np.arange(0,360 , 15):
# Calculate the Matrix
        M = cv.getRotationMatrix2D((img.shape[1]//2, img.shape[0]//2), angle, 1.0)
        # Apply the Matrix to the image
        rotated_img = cv.warpAffine(img, M, (img.shape[1], img.shape[0]))
        cv.imshow("Rotate1", rotated_img)
        cv.waitKey(200)
except:
    print("Error in rotation using cv.getRotationMatrix2D")
    
for angle in np.arange(0,360,15):
    image = imutils.rotate_bound(img , angle)
    cv.imshow("Rotate2", image)
    cv.waitKey(200)
    

cv.destroyAllWindows()