import cv2 as cv
from chapter3 import stackImages
import numpy as np
cap = cv.VideoCapture("http://192.168.1.203:8080/video") 
# cap.set(10 , 150) # Set brightness to 150
def PreProcess(frame):
    imgGray = cv.cvtColor(frame , cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(imgGray , (5,5) , 1)
    canny = cv.Canny(img_blur , 50 , 150)
    kernel = np.ones((7,7) , np.uint8)
    dilated = cv.dilate(canny , kernel , iterations=2)
    # eroded = cv.erode(dilated , kernel , iterations=1)
    return dilated

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
width = 500
height = 600
while True:
    ret, frame = cap.read()   
    frame = cv.resize(frame, (width, height) , interpolation=cv.INTER_AREA) 
    imgThres = PreProcess(frame)
    final = stackImages(0.6 , ([frame , imgThres]))
    final = cv.flip(final, 1)
    if not ret:
        print("Error: Failed to capture image.")
        break
    cv.imshow('Webcam', final)
    if cv.waitKey(30) & 0xFF == ord('q'):
        break
print("cap.cv.PROP_FPS :" , cap.get(cv.CAP_PROP_FPS))
cap.release()
cv.destroyAllWindows()
