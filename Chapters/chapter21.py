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
    cv2.imshow("Result" , imutils.resize(frame , width= 500))
    cv2.imshow("source" , imutils.resize(cv2.imread(args["source"]) , width= 500))
    cv2.imshow("target" , imutils.resize(cv2.imread(args["target"]) , width= 500))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
"""
Option 1: Compute the mean and standard deviation of the source image in a smaller region of interest (ROI) that you would like to mimic the color of, rather than using the entire image. Taking this approach will make your mean and standard deviation better represent the color space you want to use.

Option 2: The second approach is to apply k-means to both of the images. You can cluster on the pixel intensities of each image in the L*a*b* color space and then determine the centroids between the two images that are most similar using the Euclidean distance. Then, compute your statistics within each of these regions only. Again, this will give your mean and standard deviation a more “local” effect and will help mitigate the overrepresentation problem of global statistics. Of course, the downside is that this approach is substantially slower, since you have now added in an expensive clustering step.
"""

