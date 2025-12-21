import cv2 as cv
import numpy as np

def empty(x): # 
    pass

# 1. Read image ONCE (Efficiency)
path = "../Data/diffcolorcircle.png"
img = cv.imread(path)
img = cv.resize(img, (500,500))

cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 240)

# 2. Fix Initial Values (Min=0, Max=255/179)
cv.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)
cv.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv.createTrackbar("Sat Min", "Trackbars", 0, 255, empty) # Start at 0
cv.createTrackbar("Sat Max", "Trackbars", 255, 255, empty) # Start at 255
cv.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

while True:
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 3. Get ALL values (not just Hue Min)
    h_min = cv.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv.getTrackbarPos("Val Max", "Trackbars")

    # 4. Create the Mask (This is the whole point of color detection)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv.inRange(img_hsv, lower, upper)

    # Show result
    cv.imshow("Original", img)
    cv.imshow("HSV", img_hsv)
    cv.imshow("Mask", mask) # Show the black/white detection
    # The "Bitwise AND" operation
    # It says: "Take the Original Image, but only show pixels where the Mask is White."
    result = cv.bitwise_and(img, img, mask=mask)

    cv.imshow("Result", result) # Look at THIS window

    # 5. Fix the Loop Speed (1ms wait)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()