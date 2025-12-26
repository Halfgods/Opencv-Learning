import cv2
import numpy as np
import imutils
def smart_color_transfer(source, target):
    # 1. Convert to L*a*b* space
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
    target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)

    # --- THE SMART PART (YOUR IDEA) ---
    # Instead of the whole image, we create a mask for the "Sky" (Bright areas)
    # We look at the 'L' channel (Lightness)
    l_channel, a_channel, b_channel = cv2.split(source_lab)
    
    # Logic: Sky is usually the brightest part. Let's take the top 30% brightest pixels.
    # We threshold the L channel to find bright spots.
    brightness_threshold = 150 # Adjust this based on your image (0-255)
    _, mask = cv2.threshold(l_channel, brightness_threshold, 255, cv2.THRESH_BINARY)
    
    # 2. Compute Stats using the Mask!
    # cv2.meanStdDev has a 'mask' argument. It will IGNORE black pixels in the mask.
    # This captures the "Vibe" of the sky only.
    (lMeanSrc, lStdSrc) = cv2.meanStdDev(source_lab, mask=mask)
    
    # For the target, we usually want to apply it to the whole image, 
    # so we get global stats for the target (or you could mask this too!)
    (lMeanTar, lStdTar) = cv2.meanStdDev(target_lab)

    # 3. Split channels to do the math
    (l, a, b) = cv2.split(target_lab)
    
    # Helper function to scale a channel
    def scale_channel(target_channel, tar_mean, tar_std, src_mean, src_std):
        return ((target_channel - tar_mean) * (src_std / tar_std)) + src_mean

    # 4. Apply the color transfer math
    # Note: We index [0][0] because meanStdDev returns a weird [[value]] format
    l = scale_channel(l, lMeanTar[0][0], lStdTar[0][0], lMeanSrc[0][0], lStdSrc[0][0])
    a = scale_channel(a, lMeanTar[1][0], lStdTar[1][0], lMeanSrc[1][0], lStdSrc[1][0])
    b = scale_channel(b, lMeanTar[2][0], lStdTar[2][0], lMeanSrc[2][0], lStdSrc[2][0])

    # 5. Clip and Merge
    l = np.clip(l, 0, 255).astype("uint8")
    a = np.clip(a, 0, 255).astype("uint8")
    b = np.clip(b, 0, 255).astype("uint8")

    result_lab = cv2.merge([l, a, b])
    result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)
    
    return result_bgr, mask

# --- RUN IT ---
source = imutils.resize(cv2.imread("./images/night.png"), width=400)
target = imutils.resize(cv2.imread("./images/clearsky.png") , width=400)  

result, debug_mask =smart_color_transfer(source, target)
result = imutils.resize(result , width=400)
cv2.imshow("Source", source)
cv2.imshow("target", target)
cv2.imshow("Smart Mask (What it learned from)", debug_mask)
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()