import cv2
import numpy as np

# Paths to the MP4 videos
video0_path = '/home/sicb_pi/buzzCam/cam0.h264'
video1_path = '/home/sicb_pi/buzzCam/cam1.h264'

# Open the two video files
cap0 = cv2.VideoCapture(video0_path)
cap1 = cv2.VideoCapture(video1_path)

if not cap0.isOpened() or not cap1.isOpened():
    print("Error opening video files.")
    exit()

# Get video properties
width = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create display window
window_name = "Synchronized Video Playback (press 'q' to quit, space/arrow to step)"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

frame_idx = 0
while True:
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    if not ret0 or not ret1:
        print("End of video or read error.")
        break

    # Resize to match if needed (they should match already)
    if frame0.shape != frame1.shape:
        frame1 = cv2.resize(frame1, (frame0.shape[1], frame0.shape[0]))

    # Concatenate the two frames side by side
    combined = np.hstack((frame0, frame1))

    # Overlay frame number
    cv2.putText(combined, f"Frame {frame_idx}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # Show the combined frame
    cv2.imshow(window_name, combined)

    # Wait for key input (0 = wait indefinitely)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break
    elif key in [ord(' '), 83, 81, 82, 84]:  # space or arrow keys
        frame_idx += 1
        continue
    else:
        print("Press space or arrow keys to advance, 'q' to quit.")

# Release resources
cap0.release()
cap1.release()
cv2.destroyAllWindows()
