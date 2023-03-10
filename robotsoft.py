import time
import pyaudio
import wave
import replicate
import openai
import os
import re
from gtts import gTTS

from dotenv import load_dotenv
load_dotenv()
OAIKEY = os.getenv('OAIkey')
APITOKEN=os.getenv('Apitoken')

def sendToModule():
    import os
    os.environ["REPLICATE_API_TOKEN"] = APITOKEN# TOKEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




    model = replicate.models.get("openai/whisper")
    version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#input
    inputs = {
        # Audio file
        'audio': open("nagranie.wav", "rb"),#D:\\stu\\prog\\python\\bot\\

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
    prompt = re.sub('^(.*Bocie)',"", raw_prompt, count=1, flags=re.IGNORECASE)
    print ("prompt: ",prompt)

    # keysList = list(output.keys())
    # print(keysList)

    #############################################################################################################

    previous_response = "Jeste?? ??miesznym robotem w kole naukowym stworzonym przez Naukowe Ko??o Robotyki i Sztucznej Interligencji. Teraz odpowiedz na moje pytanie: "
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

    #print("reply: ",reply)







    #############################################################################################################


    #from gtts import gTTS
    #import os

    language = 'pl'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=reply, lang=language, slow=False)


    myobj.save("play.mp3")

    print("done")
    os.system("mpg321 -a plughw:2,0 play.mp3")





# ustalenie sta??ych
CHUNK = 2**12
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
THRESHOLD = 400  # warto???? progowa amplitudy, powy??ej kt??rej nagrywamy
WAIT_TIME = 0.2  # czas oczekiwania na kolejny sygna?? powy??ej progu

# inicjalizacja obiekt??w PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=1, frames_per_buffer=CHUNK)

print("Rozpoczynam nas??uchiwanie...")

# zmienne pomocnicze
frames = []
recording = False
silence_count = 0

while True:
    # odczytanie pr??bek audio z urz??dzenia
    data = stream.read(CHUNK)

    # konwersja bajt??w do tablicy numpy z warto??ciami amplitud
    audio_data = [abs(int.from_bytes(data[i:i + 2], byteorder='little', signed=True)) for i in range(0, len(data), 2)]
    amplitude = max(audio_data)

    if not recording and amplitude > THRESHOLD:
        print("Wykryto sygna?? powy??ej progu. Rozpoczynam nagrywanie...")
        recording = True

    if recording:
        frames.append(data)

        if amplitude < THRESHOLD:
            silence_count += 1

            if silence_count * WAIT_TIME >= RECORD_SECONDS:
                print("Przesta??em nagrywa??.")
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
                os.system("mpg321 -a plughw:2,0 nagranie.wav")
                #sendToModule()
        else:
            silence_count = 0
    else:
        silence_count = 0

# zako??czenie pracy
stream.stop_stream()
stream.close()
p.terminate()
