import time
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from PIL import Image
import numpy as np

# Initialize both cameras
cam0 = Picamera2(0)
cam1 = Picamera2(1)

# Sync mode configuration
ctrls = {"SyncMode": controls.rpi.SyncModeEnum.Server, "FrameRate": 30}
config0 = cam0.create_still_configuration(controls=ctrls, main={"size": (640, 480), "format": "RGB888"})
config1 = cam1.create_still_configuration(controls=ctrls, main={"size": (640, 480), "format": "RGB888"})
cam0.configure(config0)
cam1.configure(config1)

# Dummy encoders just for sync.wait()
encoder0 = H264Encoder()
encoder1 = H264Encoder()
encoder0.sync_enable = True
encoder1.sync_enable = True

# Start both cameras
cam0.start()
cam1.start()

print("Waiting for camera synchronization...")
encoder0.sync.wait()
encoder1.sync.wait()
print("Cameras synchronized!")

# Capture synchronized stills
frame0 = cam0.capture_array()
frame1 = cam1.capture_array()

# Save as images using PIL
Image.fromarray(frame0).save("cam0_sync.jpg")
Image.fromarray(frame1).save("cam1_sync.jpg")

print("Saved synchronized frames: cam0_sync.jpg, cam1_sync.jpg")

# Clean up
cam0.stop()
cam1.stop()
