import cv2
import threading


class CameraThread:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.ret, self.frame = self.capture.read()
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.capture.read()

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.capture.release()

# Usage
cam = CameraThread(0)
while True:
    frame = cam.get_frame()
    if frame is not None:
        cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.stop()
cv2.destroyAllWindows()
