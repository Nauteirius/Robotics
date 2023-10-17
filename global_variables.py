import pyaudio

CHUNK = 2**12
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
THRESHOLD = 1680  # wartość progowa amplitudy, powyżej której nagrywamy
WAIT_TIME = 0.33  # czas oczekiwania na kolejny sygnał powyżej progu