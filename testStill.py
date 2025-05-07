import time
import cv2
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# Initialize both cameras
cam0 = Picamera2(0)
cam1 = Picamera2(1)

# Configure sync mode
ctrls = {"SyncMode": controls.rpi.SyncModeEnum.Server, "FrameRate": 30}
config0 = cam0.create_still_configuration(controls=ctrls, main={"size": (640, 480)})
config1 = cam1.create_still_configuration(controls=ctrls, main={"size": (640, 480)})
cam0.configure(config0)
cam1.configure(config1)

# Create dummy encoders just to access sync.wait()
encoder0 = H264Encoder()
encoder1 = H264Encoder()
encoder0.sync_enable = True
encoder1.sync_enable = True

# Start both cameras
cam0.start()
cam1.start()

print("Waiting for sync...")
encoder0.sync.wait()
encoder1.sync.wait()
print("Cameras synchronized!")

# Capture synchronized still frames
frame0 = cam0.capture_array()
frame1 = cam1.capture_array()

# Combine and display
preview = cv2.hconcat([frame0, frame1])
cv2.imshow("Synchronized Frames", preview)
print("Showing synchronized frames. Press any key to close.")
cv2.waitKey(0)

# Cleanup
cv2.destroyAllWindows()
cam0.stop()
cam1.stop()
