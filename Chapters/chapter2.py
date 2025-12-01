# lets try doing some video processiongs

import cv2 as cv

try:
    cap = cv.VideoCapture(0) #for webcam input
    while True:
        ret, frame = cap.read()
        cv.imshow('Webcam', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
except:
    print("Cannot access webcam")