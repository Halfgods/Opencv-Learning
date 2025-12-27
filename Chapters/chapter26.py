import cv2 as cv
import numpy as np
import argparse
import imutils

def get_four_corners_iterative(contour):
    """Method 1: Loop epsilon until we find 4 points"""
    peri = cv.arcLength(contour, True)
    # Range from 0.01 to 0.10 in steps
    for eps in np.linspace(0.01, 0.10, 10):
        approx = cv.approxPolyDP(contour, eps * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)
    return None # Failed to find exactly 4

def get_min_area_rect(contour):
    """Method 2: Force a perfect rotated rectangle"""
    rect = cv.minAreaRect(contour)
    box = cv.boxPoints(rect)
    return np.int32(box)

def get_convex_hull_approx(contour):
    """Method 3: Convex Hull first, then Approx"""
    hull = cv.convexHull(contour)
    peri = cv.arcLength(hull, True)
    # Usually hull needs less strict epsilon
    approx = cv.approxPolyDP(hull, 0.04 * peri, True)
    if len(approx) == 4:
        return approx.reshape(4, 2)
    return approx.reshape(-1, 2) # Return whatever it found

def get_top_4_farthest(contour):
    """Method 4: Sort points by distance from center"""
    # 1. Calculate Center (Moment)
    M = cv.moments(contour)
    if M["m00"] == 0: return None
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    # 2. Calculate Distance for every point in contour
    # contour shape is (N, 1, 2). We want (N, 2)
    pts = contour.reshape(-1, 2)
    
    # Euclidean distance: sqrt((x1-x2)^2 + (y1-y2)^2)
    # We can just use squared distance to sort (faster)
    distances = np.sum((pts - np.array([cX, cY]))**2, axis=1)
    
    # 3. Sort and keep top 4 indices
    # argsort gives indices of sorted elements. [::-1] reverses it (Desc)
    top_indices = np.argsort(distances)[::-1][:4]
    
    # Get the actual points
    four_pts = pts[top_indices]
    return four_pts

# --- MAIN PIPELINE ---

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default="./images/scan.jpeg", help="Path to the image")
args = vars(ap.parse_args())

img = cv.imread(args["image"])
if img is None:
    print("Error: Image not found.")
    exit()

# Resize for consistency
img = imutils.resize(img, height=600)
final_viz = img.copy()

# Preprocessing
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (5,5), 0)
# Simple Otsu
ret, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

# Find Contours
cnts, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

if len(cnts) > 0:
    # Get Largest Contour
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    largest = cnts[0]

    # --- APPLY ALL 4 METHODS ---

    # 1. BLUE: MinAreaRect (Always works, but might include background)
    box_rect = get_min_area_rect(largest)
    cv.drawContours(final_viz, [box_rect], -1, (255, 0, 0), 2) # Blue

    # 2. RED: Convex Hull (Good for dented papers)
    hull_pts = get_convex_hull_approx(largest)
    if len(hull_pts) == 4:
        cv.drawContours(final_viz, [hull_pts], -1, (0, 0, 255), 2) # Red

    # 3. YELLOW: Top 4 Farthest (Your "Unpopular Opinion")
    farthest_pts = get_top_4_farthest(largest)
    if farthest_pts is not None:
        for pt in farthest_pts:
            cv.circle(final_viz, tuple(pt), 8, (0, 255, 255), -1) # Yellow Dots

    # 4. GREEN: Iterative Approx (The "Smart Loop")
    iter_pts = get_four_corners_iterative(largest)
    if iter_pts is not None:
        cv.drawContours(final_viz, [iter_pts], -1, (0, 255, 0), 3) # Thick Green

    # Draw Legend
    cv.putText(final_viz, "Green: Iterative Approx", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv.putText(final_viz, "Blue: MinAreaRect", (10, 55), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv.putText(final_viz, "Red: Convex Hull", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv.putText(final_viz, "Yellow: Top-4 Dist", (10, 105), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv.imshow("Comparison of 4 Methods", final_viz)
    cv.imshow("Thresh", thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("No contours found!")