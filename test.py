import time
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# Initialize two cameras
cam0 = Picamera2(0)
cam1 = Picamera2(1)

# Define frame sync controls
ctrlsServer = {"SyncMode": controls.rpi.SyncModeEnum.Server, "FrameRate": 30}
ctrlsClient = {"SyncMode": controls.rpi.SyncModeEnum.Client, "FrameRate": 30}

# Create and configure video configurations
config0 = cam0.create_video_configuration(controls=ctrlsServer)
config1 = cam1.create_video_configuration(controls=ctrlsClient)
cam0.configure(config0)
cam1.configure(config1)

# Set up encoders and enable sync
encoder0 = H264Encoder(bitrate=5000000)
encoder1 = H264Encoder(bitrate=5000000)
encoder0.sync_enable = True
encoder1.sync_enable = True

# Output paths
output0 = "cam0.h264"
output1 = "cam1.h264"

# Start recording on both cameras
cam0.start_recording(encoder0, output0)
cam1.start_recording(encoder1, output1)

# Wait for hardware sync
print("Waiting for synchronized start...")
encoder0.sync.wait()
encoder1.sync.wait()
print("Synchronized recording started.")

# Record for 10 seconds
time.sleep(5)

# Stop both recordings
cam0.stop_recording()
cam1.stop_recording()
print("Recording finished.")

#Delay
time.sleep(20)
# Wait for hardware sync
cam0.start_recording(encoder0, 'delay0.h264')
cam1.start_recording(encoder1, 'delay1.h264')

# Record for 10 seconds
time.sleep(5)

# Stop both recordings
cam0.stop_recording()
cam1.stop_recording()
print("Recording finished.")


