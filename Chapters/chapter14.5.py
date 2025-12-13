import cv2
import numpy as np

def nothing(x):
    # This is a dummy function required by the trackbar
    pass

# --- 1. Load Image ---
image_path = './Data/TARGET.png'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Create a dummy image if file not found (Geometric shapes)
if img is None:
    print("Image not found, creating a dummy image...")
    img = np.zeros((400, 400), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (350, 350), (255), 2) # White square outline
    cv2.circle(img, (200, 200), 100, (255), -1)        # 
    cv2.line(img, (0, 0), (400, 400), (255), 3)        # Diagonal line

# --- 2. Pre-calculate Sobel Gradients ---
# We calculate these ONCE so the loop is fast.
# Sobel X: Vertical edges
sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
# Sobel Y: Horizontal edges
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

# Convert to Absolute values (0-255) for visualization
abs_x = cv2.convertScaleAbs(sobel_x)
abs_y = cv2.convertScaleAbs(sobel_y)

# --- 3. Create Window and Trackbars ---
cv2.namedWindow('Gradient Mixer')

# Trackbar for Alpha (Sobel X Weight). Range 0-100 (representing 0.0 to 1.0)
cv2.createTrackbar('Alpha (Vert)', 'Gradient Mixer', 50, 100, nothing)

# Trackbar for Beta (Sobel Y Weight). Range 0-100 (representing 0.0 to 1.0)
cv2.createTrackbar('Beta (Horiz)', 'Gradient Mixer', 50, 100, nothing)

# Trackbar for Gamma (Brightness bias). Range 0-100
cv2.createTrackbar('Gamma', 'Gradient Mixer', 0, 100, nothing)

print("Controls:")
print(" - Slide 'Alpha' to see Vertical edges")
print(" - Slide 'Beta' to see Horizontal edges")
print(" - Slide 'Gamma' to increase base brightness")
print(" - Press 'q' to exit")

# --- 4. The Loop ---
while True:
    # Get current positions of the trackbars
    alpha_val = cv2.getTrackbarPos('Alpha (Vert)', 'Gradient Mixer')
    beta_val = cv2.getTrackbarPos('Beta (Horiz)', 'Gradient Mixer')
    gamma_val = cv2.getTrackbarPos('Gamma', 'Gradient Mixer')

    # Normalize the values (Slider is 0-100, we need 0.0-1.0)
    alpha = alpha_val / 100.0
    beta = beta_val / 100.0
    
    # Calculate the weighted sum
    # Equation: dst = src1*alpha + src2*beta + gamma
    combined = cv2.addWeighted(abs_x, alpha, abs_y, beta, gamma_val)

    # Show the result
    cv2.imshow('Gradient Mixer', combined)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

'''
We usually take alpha and beta as 0.5 
Do we hardcode these values?
In Production (Real Apps): No. For a robust document scanner, we rarely rely on addWeighted with fixed numbers because lighting changes too much.
Instead, we use Magnitude Calculation (The "True" Math): This adapts to any strength automatically without needing alpha/beta tuning.
'''