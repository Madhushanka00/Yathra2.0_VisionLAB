import queue
import cv2
import numpy as np
import time
import threading
import TreadingCamwithQ  # Import the CameraThread class from TreadingCamwithQ.py

def remove_blue(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the range for blue color in HSV
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([150, 255, 255])
    
    # Create a mask for blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Invert the mask to get everything except blue
    mask_inv = cv2.bitwise_not(mask)
    
    # Use the mask to remove blue parts from the frame
    result = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # result= mask_inv
    
    return result

def process_frame(frame_queue, processed_queue):
    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        processed_frame = remove_blue(frame)
        processed_queue.put(processed_frame)


def main():
    # Open a video capture
    cam = TreadingCamwithQ.CameraThread(0)

    frame_queue = queue.Queue(maxsize=1)
    processed_queue = queue.Queue(maxsize=1)

    processing_thread = threading.Thread(target=process_frame, args=(frame_queue, processed_queue))
    processing_thread.start()
    
    prev_time = time.time()

    while True:
        frame = cam.get_frame()
        if frame is not None:

            if not frame_queue.full():
                frame_queue.put(frame)
            
            if not processed_queue.empty():
                processed_frame = processed_queue.get()
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time)
                prev_time = curr_time

                print("Frame rate: ", fps)
                cv2.putText(processed_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Display the frame
                cv2.imshow('Video Stream without Blue', processed_frame)

        key= cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break
    # Release the video capture and close all windows
    frame_queue.put(None)
    processing_thread.join()
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()