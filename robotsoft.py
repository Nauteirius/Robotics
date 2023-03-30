import time
import pyaudio
import wave
import replicate
import openai
import os
import re
from gtts import gTTS
import random
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

from dotenv import load_dotenv
load_dotenv()
OAIKEY = os.getenv('OAIkey')
APITOKEN=os.getenv('Apitoken')

# OLED Initialization
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def displayImage(name):
    image = Image.open(name).convert('1')
    image = image.resize((128, 64))
    device.display(image)

def sendToModule():
    import os
    os.environ["REPLICATE_API_TOKEN"] = APITOKEN# TOKEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




    model = replicate.models.get("openai/whisper")
    version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#input
    inputs = {
        # Audio file
        'audio': open("nagranie.wav", "rb"),

        # Choose a Whisper model.
        'model': "large",

        # Choose the format for the transcription
        'transcription': "plain text",

        # Translate the text to English when set to True
        'translate': False,

        # language spoken in the audio, specify None to perform language
        # detection
         'language': "pl",

        # temperature to use for sampling
        'temperature': 0,

        # optional patience value to use in beam decoding, as in
        # https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to
        # conventional beam search
        # 'patience': ...,

        # comma-separated list of token ids to suppress during sampling; '-1'
        # will suppress most special characters except common punctuations
        'suppress_tokens': "-1",

        # optional text to provide as a prompt for the first window.
        # 'initial_prompt': ...,

        # if True, provide the previous output of the model as a prompt for
        # the next window; disabling may make the text inconsistent across
        # windows, but the model becomes less prone to getting stuck in a
        # failure loop
        'condition_on_previous_text': True,

        # temperature to increase when falling back when the decoding fails to
        # meet either of the thresholds below
        'temperature_increment_on_fallback': 0.2,

        # if the gzip compression ratio is higher than this value, treat the
        # decoding as failed
        'compression_ratio_threshold': 2.4,

        # if the average log probability is lower than this value, treat the
        # decoding as failed
        'logprob_threshold': -1,

        # if the probability of the <|nospeech|> token is higher than this
        # value AND the decoding has failed due to `logprob_threshold`,
        # consider the segment as silence
        'no_speech_threshold': 0.6,
    }

    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
    output = version.predict(**inputs)
    raw_prompt = output['transcription']
    print("decoded: " + raw_prompt)


    #import re
    keywords = re.compile('Bocie|bocie')
    if not keywords.search(raw_prompt):
        displayImage("default.jpg")
        return #czy zadziala
    prompt = re.sub('^(.*Bocie)',"", raw_prompt, count=1, flags=re.IGNORECASE)
    print ("prompt: ",prompt)
    keywords = re.compile('Zaśmiej się|zaśmiej się')
    keywords1 = re.compile('Puść muzykę|puść muzykę')
    if keywords.search(prompt):
        displayImage("laugh.jpg")
        os.system("mpg321 -a plughw:2,0 laugh.mp3")
        return
    elif keywords1.search(prompt):
        rng = random.ranint(1, 6)
        rng = str(rng)
        displayImage("hearth"+rng+".jpg")
        os.system("mpg321 -a plughw:2,0 soul" + rng + ".mp3")
        return


    # keysList = list(output.keys())
    # print(keysList)

    #############################################################################################################

    previous_response = "Jesteś śmiesznym robotem w kole naukowym stworzonym przez Naukowe Koło Robotyki i Sztucznej Interligencji. Teraz odpowiedz na moje pytanie: "
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt= previous_response + prompt,
        api_key=OAIKEY,
        max_tokens=200,
        n=1
    )

    reply=""
    if response is not None:
        for choice in response.choices:
            reply= choice.text[:min(2000, len(choice.text))]

    print("reply: ",reply)







    #############################################################################################################


    #from gtts import gTTS
    #import os

    language = 'pl'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=reply, lang=language, slow=False)

    displayImage("talk.jpg")
    myobj.save("play.mp3")

    print("done")
    os.system("mpg321 -a plughw:2,0 play.mp3")





# ustalenie stałych
CHUNK = 2**12
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
THRESHOLD = 1680  # wartość progowa amplitudy, powyżej której nagrywamy
WAIT_TIME = 0.33  # czas oczekiwania na kolejny sygnał powyżej progu



# inicjalizacja obiektów PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=1, frames_per_buffer=CHUNK)

displayImage("default.jpg")
print("Rozpoczynam nasłuchiwanie...")

# zmienne pomocnicze
frames = []
recording = False
silence_count = 0

while True:
    # odczytanie próbek audio z urządzenia
    data = stream.read(CHUNK)

    # konwersja bajtów do tablicy numpy z wartościami amplitud
    audio_data = [abs(int.from_bytes(data[i:i + 2], byteorder='little', signed=True)) for i in range(0, len(data), 2)]
    amplitude = max(audio_data)

    if not recording and amplitude > THRESHOLD:
        displayImage("listening.jpg")
        print("Wykryto sygnał powyżej progu. Rozpoczynam nagrywanie...")
        recording = True

    if recording:
        frames.append(data)

        if amplitude < THRESHOLD:
            silence_count += 1

            if silence_count * WAIT_TIME >= RECORD_SECONDS:
                displayImage("processing.jpg")
                print("Przestałem nagrywać.")
                recording = False
                # zapis do pliku
                wf = wave.open("nagranie.wav", "wb")
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))
                wf.close()
                # wyczyszczenie bufora
                frames = []
                #os.system("mpg321 -a plughw:2,0 nagranie.wav")
                sendToModule()
        else:
            silence_count = 0
    else:
        silence_count = 0

# zakończenie pracy
stream.stop_stream()
stream.close()
p.terminate()
