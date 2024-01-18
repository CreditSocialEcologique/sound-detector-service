import sounddevice as sd
import numpy as np
from datetime import datetime

loudness_limit = 2  # in dB
detected = False
number_of_seconds_since_loud_sound = 0
number_of_seconds_since_silence = 0
number_of_seconds_before_warning = 2
number_of_seconds_before_reset = 2
number_of_seconds_before_police = 5

def callback(indata, frames, time, status):
    global detected
    if status:
        print(status, flush=True)
    volume_norm = np.linalg.norm(indata) * 10
    print(f"Microphone input volume: {volume_norm:.2f} dB")
    if volume_norm > loudness_limit:
        #print("Loud sound detected!")
        detected = True
    else:
        detected = False

duration = 10  # in seconds
sample_rate = 44100
interval = 1
warned = False
multiplicateur = 1

with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
    while True:
        sd.sleep(int(interval * 1000))
        current_time = datetime.now().hour
        if current_time > 22 or current_time < 7:
            multiplicateur = 2
        else:
            multiplicateur = 1
        if detected:
            number_of_seconds_since_silence = 0
            number_of_seconds_since_loud_sound += multiplicateur
            if not warned and number_of_seconds_since_loud_sound > number_of_seconds_before_warning:
                print("WARNING: Loud sound detected for more than 10 seconds!")
                warned = True
            if number_of_seconds_since_loud_sound > number_of_seconds_before_police:
                print("WARNING: Police have been notified!")
                number_of_seconds_since_loud_sound = 0
        else:
            number_of_seconds_since_silence += 1
            if number_of_seconds_since_silence > number_of_seconds_before_reset:
                print("Resetting...")
                number_of_seconds_since_loud_sound = 0
                number_of_seconds_since_silence = 0
                warned = False
            detected = False