# How to create image montages using OpenCV and imutils. aka collage
from imutils import paths,build_montages
import cv2 as cv
import argparse
import random

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,help="path to input directory of images")
ap.add_argument("-s", "--sample", type=int, default=21,	help="# of images to sample")
args = vars(ap.parse_args())

# grab the paths to the images, then randomly select a sample of
# them
imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]

images = []
for imagePath in imagePaths:
    img = cv.imread(imagePath)
    images.append(img)
# build a montage using 128x128 "tiles" with 5 rows and 5 columns
montage = build_montages(images , (128,128) , (7,3))
for montages in montage:
    cv.imshow("Montage", montages)
    cv.waitKey(0)