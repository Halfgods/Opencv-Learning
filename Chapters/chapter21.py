# Color transfer functions for images.
# import the necessary packages
import numpy as np
import cv2
import argparse
import imutils
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
    help="path to the source image")
ap.add_argument("-t", "--target", required=True,
    help="path to the target image")
args = vars(ap.parse_args())

def color_transfer(source, target):
	# convert the images from the RGB to L*ab* color space, being
	# sure to utilizing the floating point data type (note: OpenCV
	# expects floats to be 32-bit, so use that instead of 64-bit)
	source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
	target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")
    # compute color statistics for the source and target images
	(lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
	(lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)
	# subtract the means from the target image
	(l, a, b) = cv2.split(target)
	l -= lMeanTar
	a -= aMeanTar
	b -= bMeanTar
	# scale by the standard deviations
	l = (lStdTar / lStdSrc) * l
	a = (aStdTar / aStdSrc) * a
	b = (bStdTar / bStdSrc) * b
	# add in the source mean
	l += lMeanSrc
	a += aMeanSrc
	b += bMeanSrc
	# clip the pixel intensities to [0, 255] if they fall outside
	# this range
	l = np.clip(l, 0, 255)
	a = np.clip(a, 0, 255)
	b = np.clip(b, 0, 255)
	# merge the channels together and convert back to the RGB color
	# space, being sure to utilize the 8-bit unsigned integer data
	# type
	transfer = cv2.merge([l, a, b])
	transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)
	
	# return the color transferred image
	return transfer

def image_stats(image):
	# compute the mean and standard deviation of each channel
	(l, a, b) = cv2.split(image)
	(lMean, lStd) = (l.mean(), l.std())
	(aMean, aStd) = (a.mean(), a.std())
	(bMean, bStd) = (b.mean(), b.std())
	# return the color statistics
	return (lMean, lStd, aMean, aStd, bMean, bStd)

if __name__ == "__main__":
    frame = color_transfer(cv2.imread(args["source"]), cv2.imread(args["target"]))
    cv2.imshow("Result" , imutils.resize(frame , width= 400))
    cv2.imshow("source" , imutils.resize(cv2.imread(args["source"]) , width= 400))
    cv2.imshow("target" , imutils.resize(cv2.imread(args["target"]) , width= 400))
    cv2.waitKey(0)
    