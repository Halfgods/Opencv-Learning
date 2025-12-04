import cv2 as cv
import matplotlib.pyplot as plt
import math
imagefiles = ["./boat/boat1.jpg" , "./boat/boat2.jpg" , "./boat/boat3.jpg" , "./boat/boat4.jpg" , "./boat/boat5.jpg" , "./boat/boat6.jpg"]
images = []
for filename in imagefiles:
    img = cv.imread(filename)
    # img = cv2.cvtColor(img, cv.COLOR_BGR2RGB)
    images.append(img)

num_images = len(images)

num_cols = 3
num_rows = math.ceil(num_images / num_cols)
stitcher = cv.Stitcher_create()
status, result = stitcher.stitch(images)

if status == 0:
    # plt.figure(figsize=[30, 10])
    cv.imshow("Result",result)
cv.imwrite("./related output/learnings/boat_panorama.jpg", result)
cv.waitKey(0)
cv.destroyAllWindows()