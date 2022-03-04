#pip install pipwin
#pipwin install pyaudio
import speech_recognition as sr  #pip install SpeechRecognition
import pyttsx3  #pip install pyttsx3

# text to speech
def textTospeech(text):
    tts = pyttsx3.init("sapi5")
    voices = tts.getProperty('voices')
    tts.setProperty('rate', 140)  # set voice speed
    tts.setProperty('voice', voices[0].id)  # set voice character
    tts.say(text)
    tts.runAndWait()

# speech to text
def speechTotext(ask=""):
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        
        if ask != "":
            print(f"Com: {ask}")
            textTospeech(f"{ask}")
            print("Listening...")
        else:
            print("Listening...")

        #r.energy_threshold = 300  
        #r.dynamic_energy_threshold = True
        #r.dynamic_energy_adjustment_damping = 0.15
        #r.dynamic_energy_ratio = 1.5
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        #r.operation_timeout = None  
        #r.phrase_threshold = 0.3  
        #r.non_speaking_duration = 0.5

        speech = r.listen(source)
        text = ""
        try:
            print("Processing...")
            print("")
            text = r.recognize_google(speech, language="en-US")
            print(f"Me: {text}")
        
        except sr.UnknownValueError:
            #textTospeech("sorry, I didn't get that.")
            pass

        except sr.RequestError:
            #textTospeech("sorry, the server is down.")
            pass

    return text.lower()