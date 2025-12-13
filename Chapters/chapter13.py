import cv2 as cv
import numpy as np

def empty(x):
    pass

# 1. Read Image ONCE
path = "./Data/TARGET.png"
img_original = cv.imread(path)

# Safety Check
if img_original is None:
    print(f"Error: Could not read image at {path}. Check your path!")
    exit()

# Optional: Resize if the image is too big for your screen
img_original = cv.resize(img_original, (640, 480))
cv.namedWindow("Blur Control")
cv.resizeWindow("Blur Control", 640, 300)

# 2. Setup Trackbars
cv.createTrackbar("Method", "Blur Control", 0, 4, empty) 
cv.createTrackbar("Kernel Size", "Blur Control", 1, 30, empty) 
cv.createTrackbar("Sigma", "Blur Control", 10, 200, empty)

print("Controls active. Press 'q' to quit.")

while True:
    # 3. Read Trackbars
    method = cv.getTrackbarPos("Method", "Blur Control")
    k_val = cv.getTrackbarPos("Kernel Size", "Blur Control")
    sigma = cv.getTrackbarPos("Sigma", "Blur Control")

    # Force Kernel to be ODD (1, 3, 5...)
    k_size = k_val * 2 + 1

    # CRITICAL: Always start with a fresh copy of the original image
    img_display = img_original.copy()
    txt = "Original"

    # 4. Apply Selected Method
    if method == 0:
        txt = "Original (No Blur)"
        # Do nothing, img_display is already the original

    elif method == 1:
        txt = f"Average Blur ({k_size}x{k_size})"
        img_display = cv.blur(img_original, (k_size, k_size))

    elif method == 2:
        txt = f"Gaussian Blur ({k_size}x{k_size})"
        img_display = cv.GaussianBlur(img_original, (k_size, k_size), sigmaX=sigma/10) 

    elif method == 3:
        txt = f"Median Blur (k={k_size})"
        img_display = cv.medianBlur(img_original, k_size)

    elif method == 4:
        txt = f"Bilateral Filter (d={k_size})"
        # Limit diameter for speed
        d = k_size 
        if d > 15: d = 15 
        img_display = cv.bilateralFilter(img_original, d, sigmaColor=sigma, sigmaSpace=sigma)

    # 5. Display Text & Image
    cv.putText(img_display, txt, (20, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv.imshow("Result", img_display)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

'''
Method | Metric used to Blur | Effect on Edges | Processing Speed
Average | Pure Math (1/N) | Destroys them (Blocky) | Super Fast
Gaussian | Distance only | Blurs them (Soft) | Fast
Bilateral | Distance + Color | Preserves them (Sharp) | Very Slow
'''
