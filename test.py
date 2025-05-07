import time
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
picam2 = Picamera2()
ctrls = {'SyncMode': controls.rpi.SyncModeEnum.Server, 'FrameRate': 30}
config = picam2.create_video_configuration(controls=ctrls)
picam2.configure(config)
encoder = H264Encoder(bitrate=5000000)
encoder.sync_enable = True # enable synchronised recording
output = "server.h264"
picam2.start_recording(encoder, output)
print("Waiting for sync...")
encoder.sync.wait()
print("Recording has started")
time.sleep(5)
picam2.stop_recording()
print("Recording has finished")