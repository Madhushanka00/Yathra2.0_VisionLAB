import cv2
import threading
import queue
import warnings
import time
warnings.filterwarnings("ignore")
# a sample class to capture video from a camera
# git config

class CameraThread:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.frame_queue = queue.Queue(maxsize=1)
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                if not self.frame_queue.empty():
                    try:
                        self.frame_queue.get_nowait()  # Discard the previous frame
                    except queue.Empty:
                        pass
                self.frame_queue.put(frame)

    def get_frame(self):
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        self.running = False
        self.thread.join()
        self.capture.release()

# Usage
if __name__ == "__main__":
    cam = CameraThread(0)
    # prew_time = time.time()

    while True:
        frame = cam.get_frame()
        if frame is not None:
            cv2.imshow("Frame", frame)
        key= cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

    cam.stop()
    cv2.destroyAllWindows()