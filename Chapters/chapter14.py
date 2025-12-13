import cv2
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Load the image ---
# Load as grayscale. Gradients work on intensity changes, so color is not needed.
image_path = './Data/TARGET.png'  # Replace with your image path
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    print(f"Error: Could not load image from {image_path}")
    # Create a dummy image if the file is not found
    img = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (250, 250), (255), -1) # White square
    cv2.circle(img, (150, 150), 70, (100), -1, ) # Gray circle
    print("Created a dummy geometric image for demonstration.")
# --- 2. Apply Sobel Filters ---
# cv2.CV_64F is used to allow negative values (e.g., dark-to-bright transitions).
# dx=1, dy=0 means calculate the gradient in the X direction only.
sobel_x = cv2.Sobel(img, cv2.CV_64F, dx=1, dy=0, ksize=3)

# dx=0, dy=1 means calculate the gradient in the Y direction only.
sobel_y = cv2.Sobel(img, cv2.CV_64F, dx=0, dy=1, ksize=3)


# --- 3. Process Sobel Output for Visualization ---
# The output contains negative and positive values.
# We take the absolute value to see all edges as bright lines.
abs_sobel_x = cv2.convertScaleAbs(sobel_x)
abs_sobel_y = cv2.convertScaleAbs(sobel_y)

# Combine them to get the overall edge magnitude (approximate)
# A more accurate way is sqrt(sobel_x**2 + sobel_y**2)
sobel_combined = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)


# --- 4. Apply Laplacian Filter ---
# This is the 2nd derivative, good for finding all edges and sharpening.
laplacian = cv2.Laplacian(img, cv2.CV_64F)
# Take absolute value for visualization
abs_laplacian = cv2.convertScaleAbs(laplacian)


# --- 5. Plot the results using Matplotlib ---
plt.figure(figsize=(12, 8))

# Original Image
plt.subplot(2, 3, 1)
plt.title('Original Image (Grayscale)')
plt.imshow(img, cmap='gray')
plt.axis('off')

# Sobel X
plt.subplot(2, 3, 2)
plt.title('Sobel X (Vertical Edges)')
# Using 'bwr' (blue-white-red) colormap to show negative/positive values
plt.imshow(sobel_x, cmap='bwr')
plt.axis('off')

# Sobel Y
plt.subplot(2, 3, 3)
plt.title('Sobel Y (Horizontal Edges)')
plt.imshow(sobel_y, cmap='bwr')
plt.axis('off')

# Sobel X (Absolute)
plt.subplot(2, 3, 4)
plt.title('Sobel X (Absolute Value)')
plt.imshow(abs_sobel_x, cmap='gray')
plt.axis('off')

# Sobel Y (Absolute)
plt.subplot(2, 3, 5)
plt.title('Sobel Y (Absolute Value)')
plt.imshow(abs_sobel_y, cmap='gray')
plt.axis('off')

# Combined Sobel Magnitude
plt.subplot(2, 3, 6)
plt.title('Combined Sobel Magnitude')
plt.imshow(sobel_combined, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()

# --- Extra Plot for Laplacian ---
plt.figure(figsize=(6, 6))
plt.title('Laplacian (2nd Derivative)')
plt.imshow(abs_laplacian, cmap='gray')
plt.axis('off')
plt.show()

"""
Original Image: Your starting image in black and white.
Sobel X / Y (Raw): You'll see a gray image with blue and red lines.
    Red: A transition from dark to bright (a positive gradient).
    Blue: A transition from bright to dark (a negative gradient).
    Gray: No change (zero gradient).
Notice how Sobel X highlights vertical lines and Sobel Y highlights horizontal ones.
Sobel X / Y (Absolute): This is what's more commonly used. All transitions, regardless of direction, are shown as bright white lines against a black background.
Combined Sobel Magnitude: This combines both X and Y to give you a complete "wireframe" outline of all the edges in the image.
Laplacian: Similar to the combined Sobel, but often produces thinner, sharper lines and is more sensitive to fine details (and noise!).
"""