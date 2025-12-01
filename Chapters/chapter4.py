import cv2 as cv
import numpy as np
'''Numpy .shape returns a tuple of array dimensions (height, width)
while Opencv .resize needs dimensions in (width, height) format.'''

img = cv.imread("./Data/lena.jpg")      # The Reference (Master)
image = cv.imread("./Data/butterfly.jpg") # The One to Resize (Slave)
print(type(img))
#Written by me 
def resize_images(to_be_resized, reference):
    
    width = reference.shape[1]
    height = reference.shape[0]
    
    
    result = cv.resize(to_be_resized, (width, height), interpolation=cv.INTER_AREA)
    return result
#

image = resize_images(image, img)


Imghor = np.hstack((img, image))
Imggor = np.vstack((img, image))

cv.imshow("Horizontal Stacking", Imghor)
cv.imshow("Vertical Stacking", Imggor)
cv.waitKey(0)
cv.destroyAllWindows()