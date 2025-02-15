# testing the camera setup inraspberry Pi and navi os with OpenCV
# camera userd: Logitech Web cam 720P (Video0)
# Date: 2021-09-25

import cv2
import warnings

cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)  # Try 30 FPS

warnings.filterwarnings("ignore", category=DeprecationWarning)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
else:
    print("Camera opened")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?)")
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
