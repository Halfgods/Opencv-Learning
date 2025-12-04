import cv2 as cv
import numpy as np
scan = "./Data/scan.jpg"
scanned_output = "./Data/scanned output.png"
img1 = cv.imread(filename=scan)
img2 = cv.imread(filename=scanned_output)
gray1 = cv.cvtColor(img1 , cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(img2 , cv.COLOR_BGR2GRAY)
MAX_NUM_FEATURES = 500
orb = cv.ORB_create(nfeatures=MAX_NUM_FEATURES)
key_points1 , descriptors1 = orb.detectAndCompute(gray1 , None)
key_points2 , descriptors2 = orb.detectAndCompute(gray2 , None)
im1_display = cv.drawKeypoints(img1, key_points1, outImage=np.array([]), color=(255, 0, 0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
im2_display = cv.drawKeypoints(img2, key_points1, outImage=np.array([]), color=(255, 0, 0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Match features.
matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

# Converting to list for sorting as tuples are immutable objects.
matches = list(matcher.match(descriptors1, descriptors2, None))

# Sort matches by score
matches.sort(key=lambda x: x.distance, reverse=False)

# Remove not so good matches
numGoodMatches = int(len(matches) * 0.1)
matches = matches[:numGoodMatches]
im_matches = cv.drawMatches(img1, key_points1, img2, key_points2, matches, None)
cv.imshow("Image 1 Keypoints", im_matches)
# cv.imshow("Image 2 Keypoints", im2_display)
cv.waitKey(0)
cv.destroyAllWindows()