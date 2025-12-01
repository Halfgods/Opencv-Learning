import cv2 as cv
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
imggray = cv.imread('./Data/lena.jpg', 0)
img = cv.imread('./Data/lena.jpg')
faces = face_cascade.detectMultiScale(imggray, 1.1, 4)
for x,y,w,h in faces:
    cv.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)


cv.imshow('Original Image', img)
cv.waitKey(0)
