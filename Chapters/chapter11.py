import cv2 as cv
import numpy as np

def empty(x):
    pass

# 1. Initialize Webcam
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 240)

# 2. Fix Initial Values
cv.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)
cv.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv.createTrackbar("Sat Min", "Trackbars", 0, 255, empty)
cv.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

while True:
    success, img = cap.read()
    if not success: break

    img = cv.flip(img, 1)
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 3. Get Trackbar Values
    h_min = cv.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv.getTrackbarPos("Val Max", "Trackbars")

    # 4. Create Mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv.inRange(img_hsv, lower, upper)

    # ===================================================
    # START: TRACKING LOGIC (The new part)
    # ===================================================
    
    # a. Find Contours (Boundaries of white blobs)
    # RETR_EXTERNAL: Only outer corners (don't care about holes inside)
    # CHAIN_APPROX_SIMPLE: Stores less data (just the corner points)
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # b. Loop through every blob found
    for cnt in contours:
        # Calculate area of the blob
        area = cv.contourArea(cnt)
        
        # BRUTAL FACT: Real life has noise. 
        # Ignore tiny white dots (area < 1000) to stop the box from jittering.
        if area > 1000: 
            # c. Get the Bounding Box coordinates
            x, y, w, h = cv.boundingRect(cnt)
            
            # d. Draw the Rectangle on the ORIGINAL image
            # (Image, Start_Point, End_Point, Color_BGR, Thickness)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Optional: Add text
            cv.putText(img, "Target", (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # ===================================================
    # END: TRACKING LOGIC
    # ===================================================

    # 5. Stack and Display
    result = cv.bitwise_and(img, img, mask=mask)
    mask_3channel = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    hstack = np.hstack([img, mask_3channel, result])

    cv.imshow("Calibration Tool (Press Q to Quit)", hstack)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()