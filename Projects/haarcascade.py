import cv2 as cv

frontaface_cascade = cv.CascadeClassifier('./Projects/Models/haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)
while True:
    ret , frame = cap.read()
    frame = cv.flip(frame , 1)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = frontaface_cascade.detectMultiScale(gray, 1.5, 4)
    for(x,y,w,h) in faces:
        cv.rectangle(frame, (x,y) , (x+w , y+h) , (255,0,0) , 3)
        
    cv.imshow('Face Detection' , frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()