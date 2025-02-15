import cv2

# Create a VideoCapture object to read from the video file or camera
cap = cv2.VideoCapture(0)  # Replace 'video.mp4' with 0 to use the webcam

# Create the background subtractor object
backSub = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply the background subtractor to get the foreground mask
    fgMask = backSub.apply(frame)

    # Display the original frame and the foreground mask
    cv2.imshow('Frame', frame)
    cv2.imshow('Foreground Mask', fgMask)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()