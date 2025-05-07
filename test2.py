import time
import subprocess
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# ---- Setup ----

# Camera initialization
cam0 = Picamera2(0)
cam1 = Picamera2(1)

ctrlsServer = {"SyncMode": controls.rpi.SyncModeEnum.Server, "FrameRate": 30}
ctrlsClient = {"SyncMode": controls.rpi.SyncModeEnum.Client, "FrameRate": 30}
config0 = cam0.create_video_configuration(controls=ctrlsServer)
config1 = cam1.create_video_configuration(controls=ctrlsClient)
cam0.configure(config0)
cam1.configure(config1)

encoder0 = H264Encoder(bitrate=5000000)
encoder1 = H264Encoder(bitrate=5000000)
encoder0.sync_enable = True
encoder1.sync_enable = True

raw0 = "cam0_raw.h264"
raw1 = "cam1_raw.h264"

# ---- Start Recording ----

cam0.start_recording(encoder0, raw0)
cam1.start_recording(encoder1, raw1)

print("Waiting for synchronized start...")
encoder0.sync.wait()
encoder1.sync.wait()
print("Synchronized recording started.")

# ---- Wait for trigger ----

print("Recording... waiting for trigger. Press Enter to simulate trigger.")
input()  # Replace with sensor or other trigger logic

print("Trigger detected. Continuing for 5 more seconds...")
time.sleep(5)

# ---- Stop Recording ----
cam0.stop_recording()
cam1.stop_recording()
print("Recording stopped.")

# ---- Trim to Last 10 Seconds ----

def trim_video(input_file, output_file, duration=10):
    cmd = [
        "ffmpeg",
        "-sseof", f"-{duration}",  # seek from end
        "-i", input_file,
        "-c", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)

print("Trimming to final 10 seconds...")
trim_video("cam0_raw.h264", "cam0_trimmed.mp4", duration=10)
trim_video("cam1_raw.h264", "cam1_trimmed.mp4", duration=10)
print("Trimmed videos saved as cam0_trimmed.mp4 and cam1_trimmed.mp4")
