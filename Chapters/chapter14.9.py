import cv2

def is_image_blurry(image_path, threshold=100): # type: ignore
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Calculate Laplacian
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    
    # Calculate the Variance (The "Score" of sharpness)
    score = laplacian.var()
    
    print(f"Sharpness Score: {score:.2f}")
    
    if score < threshold:
        print("Result: BLURRY! ❌ (Please hold steady)")
    else:
        print("Result: SHARP! ✅")

# Try it with a blurry photo and a clear photo!
is_image_blurry('./Data/TARGET.png')

'''
Feature | Sobel (Gradient) | Laplacian
Math | 1st Derivative (Slope) | 2nd Derivative (Curve)
Direction | Specific (Horizontal OR Vertical) | Omni-directional (All sides)
Main Use | Finding outlines of objects (Scanner) | Blur Detection & Sharpening
Noise | Handles noise okay | Hates noise (very sensitive)
'''