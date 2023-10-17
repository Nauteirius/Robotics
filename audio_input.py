from global_variables import FORMAT, CHANNELS, RATE, CHUNK
import pyaudio

class AudioInput:
    def __init__(self) -> None:
        p = pyaudio.PyAudio()
        input_device_index = self.detect_input_device_index()
        self.stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=input_device_index, frames_per_buffer=CHUNK)
    
    def detect_input_device_index(self) -> int:
        return 1

    def read_chunk(self):
        return self.stream.read(CHUNK)