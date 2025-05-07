import cv2
import numpy as np

# Paths to video files
video0_path = 'cam0.mp4'
video1_path = 'cam1.mp4'

# Open both videos
cap0 = cv2.VideoCapture(video0_path)
cap1 = cv2.VideoCapture(video1_path)

if not cap0.isOpened() or not cap1.isOpened():
    print("Error opening one or both video files.")
    exit()

# Get total number of frames
total_frames = int(min(cap0.get(cv2.CAP_PROP_FRAME_COUNT), cap1.get(cv2.CAP_PROP_FRAME_COUNT)))

# Create display window
window_name = "Synchronized Playback: ← ↓ = back | → space = forward | q = quit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

frame_idx = 0

while True:
    # Set both video readers to the current frame
    cap0.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    cap1.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    if not ret0 or not ret1:
        print("End of video or error reading frame.")
        break

    # Resize frame1 if shape mismatch (precaution)
    if frame0.shape != frame1.shape:
        frame1 = cv2.resize(frame1, (frame0.shape[1], frame0.shape[0]))

    # Combine frames side by side
    combined = np.hstack((frame0, frame1))
    cv2.putText(combined, f"Frame {frame_idx+1}/{total_frames}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow(window_name, combined)

    # Wait for key press (0 = indefinitely)
    key = cv2.waitKey(0) & 0xFF

    # Quit
    if key == ord('q'):
        break
    # Forward: space or right arrow
    elif key in [ord(' '), 83]:  # space, →
        if frame_idx < total_frames - 1:
            frame_idx += 1
    # Backward: left or down arrow
    elif key in [81, 84]:  # ←, ↓
        if frame_idx > 0:
            frame_idx -= 1
    else:
        print("Use ← ↓ to go back, → or space to go forward, 'q' to quit.")

# Cleanup
cap0.release()
cap1.release()
cv2.destroyAllWindows()
