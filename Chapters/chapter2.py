import cv2 as cv
# 0 is usually the default webcam.
# If you have an external USB camera, try changing this to 1 or 2.
cap = cv.VideoCapture(0) 

# Check if the webcam opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # 1. Read the frame
    ret, frame = cap.read()
    
    # 2. BRUTAL FACT: Always check 'ret'. Since ret returns a bool value
    # If the camera disconnects or frame is dropped, 'ret' becomes False.
    if not ret:
        print("Error: Failed to capture image.")
        break

    # 3. Show the frame
    cv.imshow('Webcam', frame)

    # 4. Exit on 'q' key
    if cv.waitKey(30) & 0xFF == ord('q'):
        break
print("cap.cv.PROP_FPS :" , cap.get(cv.CAP_PROP_FPS))

cap.release()
cv.destroyAllWindows()

'''
Additional Notes:
we dont find any changes when doing the waitkey 1 or 30 ms
but in some systems, waitkey 1 may cause high CPU usage.
So, it's often better to use a slightly higher value like 30 ms.
This will also help in reducing CPU usage.
Also, the actual frame rate may depend on the camera hardware and lighting conditions.
The cap.get(cv.CAP_PROP_FPS) may not return the actual fps of the camera.'''