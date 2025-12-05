import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def convolution_demo():
    # Load image in Gray for clarity
    img = cv.imread("./ldr-Drago.jpg", 0) 
    if img is None:
        print("Image not found. Using a dummy image.")
        img = np.zeros((300, 300), dtype=np.uint8)
        cv.rectangle(img, (50, 50), (250, 250), 255, -1)

    # 1. THE BLUR KERNEL (What you did)
    # A box of averages. 
    k_blur = np.ones((15, 15), np.float32) / 225

    # 2. THE EDGE KERNEL (What AI uses)
    # This highlights differences between left and right pixels
    k_edge = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])

    # Apply both using the same function
    out_blur = cv.filter2D(img, -1, k_blur)
    out_edge = cv.filter2D(img, -1, k_edge)

    # Plot
    plt.figure(1)
    plt.title("Original")
    plt.imshow(img)

    plt.figure(2)
    plt.title("Your Blur (Averaging)")
    plt.imshow(out_blur)

    plt.figure(3)
    plt.title("AI Edge Feature (Sobel)")
    plt.imshow(out_edge, cmap='gray') # Note: Edges will light up white

    plt.show()

if __name__ == '__main__':
    convolution_demo()