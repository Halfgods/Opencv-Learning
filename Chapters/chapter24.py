import argparse
import imutils
import cv2

# ... (Argument parsing stays the same) ...
ap = argparse.ArgumentParser()
ap.add_argument("-i" , "--image" , default="./Chapters/shapes_and_colors.png")
args  = vars(ap.parse_args())
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# FIX 1: Unpack both values (ret, thresh)
ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
cv2.imshow("Thresh" , thresh)
print(ret)
# FIX 3: Just use standard OpenCV unpacking, remove imutils line
cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:
    M = cv2.moments(c)
    print(f"M00: {M["m00"]}")
    print(f"M01: {M["m01"]}")
    print(f"M10: {M["m10"]}")
    # FIX 2: Check for Division by Zero
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        # If contour area is 0, set center to (0,0) or skip it
        cX, cY = 0, 0 

    cv2.drawContours(image, [c], 0, (0, 255, 0), 2 )
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)