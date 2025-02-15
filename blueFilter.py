import cv2
import numpy as np
import time

# import TreadingCamwithQ

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

def main():
    # Open a video capture
    cap = cv2.VideoCapture(0)
    # cap = TreadingCamwithQ.CameraThread(0)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return
    
    prev_time = time.time()

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Remove blue parts from the frame
        frame_no_blue = remove_blue(frame)
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        print("Frame rate: ", fps)
        cv2.putText(frame_no_blue, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Video Stream without Blue', frame_no_blue)
        
         # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()




    # # Read a single image
    # image_path = "gate-2022.jpg"
    # frame = cv2.imread(image_path)
    
    # if frame is None:
    #     print("Error: Could not read image.")
    #     return
    
    # # Remove blue parts from the image
    # frame_no_blue = remove_blue(frame)
    
    # # Display the image
    # cv2.imshow('Image without Blue', frame_no_blue)
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()