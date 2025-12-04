import cv2 as cv
import numpy as np
def readImagesAndTimes():
    # List of file names
    filenames = ["./Data/img_0.033.jpg", "./Data/img_0.25.jpg", "./Data/img_2.5.jpg", "./Data/img_15.jpg"]

    # List of exposure times
    times = np.array([1 / 30.0, 0.25, 2.5, 15.0], dtype=np.float32)

    # Read images
    images = []
    for filename in filenames:
        im = cv.imread(filename)
        images.append(im)

    return images, times

images, times = readImagesAndTimes()

# Align Images
alignMTB = cv.createAlignMTB()
alignMTB.process(images, images)
# Find Camera Response Function (CRF)
calibrateDebevec = cv.createCalibrateDebevec()
responseDebevec = calibrateDebevec.process(images, times)
# Merge images into an HDR linear image
mergeDebevec = cv.createMergeDebevec()
hdrDebevec = mergeDebevec.process(images, times, responseDebevec)
tonemapDrago = cv.createTonemapDrago(1.0, 0.7)
ldrDrago = tonemapDrago.process(hdrDebevec)
ldrDrago = 3 * ldrDrago

# Saving image
cv.imwrite("ldr-Drago.jpg", 255*ldrDrago)
cv.imshow("ldr-Drago", ldrDrago)
print("Tonemaping using Reinhard's method ... ")
tonemapReinhard = cv.createTonemapReinhard(1.5, 0, 0, 0)
ldrReinhard = tonemapReinhard.process(hdrDebevec)

# Saving image
cv.imwrite("ldr-Reinhard.jpg", ldrReinhard * 255)
cv.imshow("ldr-Reinhard", ldrReinhard)

print("Tonemaping using Mantiuk's method ... ")
tonemapMantiuk = cv.createTonemapMantiuk(2.2, 0.85, 1.2)
ldrMantiuk = tonemapMantiuk.process(hdrDebevec)
ldrMantiuk = 3 * ldrMantiuk

# save the image using cv2.imwrite
cv.imwrite("ldr-Mantiuk.jpg", ldrMantiuk * 255)
cv.imshow("ldr-Mantiuk", ldrMantiuk)
cv.waitKey(0)
cv.destroyAllWindows()
