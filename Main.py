import json
import torch   #pip install torch
import random
import os
from time import sleep
import wikipedia   #pip install wikipedia
import webbrowser
import pywhatkit   #pip install pywhatkit
import cv2   #pip install opencv-contrib-python

from Brain import NeuralNet
from NeuralNetwork import bag_of_words, tokenize
from TextandSpeech import textTospeech, speechTotext
from DateandTime import current_day, current_date, current_time
from WeatherReport import weather_reports
from Jokes import joke
from MyLocation import my_location
from Screenshot import takeScreenshot
from Calculation import calculation
from Notes import takeNotes
from SendEmail import send_mail
from Identify import checkFolder, imageIdentification
from SystemSoftware import openApp

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json") as json_data:
    intents = json.load(json_data)
    
FILE = "TrainData.pth"
data = torch.load(FILE)

model_state = data["model_state"]
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

cam = cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# create face ID    
def faceID(frame):
    pic_loc = "face_identity/"
    pic_name = f"{pic_loc}user_identity.jpg"
            
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray, 1.3, 5)
            
    if face is not None:
        for (x, y, w, h) in face:
            cropped_face = frame[y:y+h, x:x+w]
        cv2.imwrite(pic_name, cropped_face)
    else:
        return None
    
# checking faceID folder
check = checkFolder()
if check == "empty":
    textTospeech("No face ID found.")
    textTospeech("Setup your face ID.")
    textTospeech("Open your face to the camera clearly and press space key. After that, wait upto 5 second to capture your face.")
elif check == "notempty":
    pass
else:
    pass  

# greetings
def greetings():
    textTospeech("Hello.")

while True:
    ret, frame = cam.read()
    
    # checking folder
    if check == "empty":
        key = cv2.waitKey(1)
        
        cv2.imshow("FaceID", frame)
                
        if key % 256 == 32:    # space key; for Esc, 27  
            sleep(1)
            faceID(frame)   # calling face ID function
            cam.release()
            cv2.destroyAllWindows()
    
    # checking folder     
    elif check == "notempty":
        identity = imageIdentification(frame)
        
        # checking face ID
        if identity == "matched":
            sleep(1)
            textTospeech("Face matched!")
            greetings()
                
            sentence = speechTotext("What do you want to say?")
            sentence_tk = tokenize(sentence)
            X = bag_of_words(sentence_tk, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)
    
            output = model(X)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            # checking probability
            if prob.item() > 0.75:
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        reply = random.choice(intent["responses"])
                
                        #---------------Time
                        if "time" in reply:
                            dateTime = current_time()
                            print(f"Com: rightnow, it is {dateTime}")
                            textTospeech(f"rightnow, it is {dateTime}")
                
                        #---------------Date    
                        elif "date" in reply:
                            dateTime = current_date()
                            weekday = current_day()
                            print(f"Com: today is {weekday}, {dateTime}")
                            textTospeech(f"today is {weekday}, {dateTime}")
                
                        #---------------Weather Report
                        elif "weatherReport" in reply:
                            city = speechTotext("which city?")
                            try:
                                if weather_reports(city) == "error":
                                    print(f"Com: invalid city ({city}), check your city name.")
                                    textTospeech(f"invalid city ({city}), check your city name.")
                                else:
                                    humidity, temp, phrase, wind = weather_reports(city)
                                    print(f"Com: currently in {city}, temperature is {str(temp)} degree celsius, humidity is {str(humidity)} percent, wind speed is {wind} m/s and the sky is {phrase}")
                                    textTospeech(f"currently in {city}, temperature is {str(temp)} degree celsius, humidity is {str(humidity)} percent, wind speed is {wind} meter per second and the sky is {phrase}")

                            except:
                                print("Com: sorry, I couldn't find that.")
                                textTospeech("sorry, I couldn't find that.")
                
                        #---------------Jokes        
                        elif "jokes" in reply:
                            joke_msg = ""
                            joke_msg = joke()
                            print(f"Com: {joke_msg}")
                            textTospeech(joke_msg)
                
                        #---------------My IP Location    
                        elif "myLocation" in reply:
                            try:
                                my_city, my_country = my_location()
                                print(f"Com: according to your ip address, we are currently in {my_city}, a city of {my_country}.")
                                textTospeech(f"according to your ip address, we are currenty in {my_city}, a city of {my_country}.")
                        
                            except Exception as e:
                                print("Com: sorry, due to network issue i'm not able to find where we are right now.")
                                textTospeech("sorry, due to network issue I'm not able to find where we are right now.")
                
                        #---------------Screenshot        
                        elif "screenshot" in reply:
                            print("Com: hold the screen for a few seconds.")
                            textTospeech("hold the screen for a few seconds.")
                            sleep(1)
                            takeScreenshot()
                            sleep(2)
                            print("Com: screen capture done. check in screenshot folder.")
                            textTospeech("screen capture done. check in screenshot folder.")
                    
                        #---------------Wikipedia
                        elif "wikipedia" in reply:
                            wiki_search = speechTotext("what do you want to search on wikipedia?")
                            print("Com: searching on wikipedia...")
                            textTospeech("searching on wikipedia...")
                            wiki_result = wikipedia.summary(wiki_search, sentences=2)
                            print("Com: according to wikipedia...")
                            textTospeech("according wikipedia")
                            print(f"Com: {wiki_result}")
                            textTospeech(wiki_result)
                    
                        #---------------Google Search
                        elif "googleSearch" in reply:
                            print("Com: what should I search on google?")
                            textTospeech("what should I search on google?")
                            search_key = speechTotext()
                            webbrowser.get().open(f"https://google.com/search?q={search_key}")
                    
                        #---------------Calculation
                        elif "calculation" in reply:
                            cal_queue = speechTotext("what you want to calculate?")
                            result = calculation(cal_queue)
                            print(f"Com: result is {result}")
                            textTospeech(f"result is {result}")
                    
                        #---------------Notes
                        elif "notes" in reply:
                            filename = speechTotext("what wiil be the file name?")
                            notes = speechTotext("what do you want to write?")
                            takeNotes(filename, notes)
                            sleep(2)
                            print("Com: the note is saved. check in Notepad folder.")
                            textTospeech("the note is saved. check in Notepad folder.")
                    
                        #---------------Play Music from YT
                        elif "playYT" in reply:
                            song = sentence.replace("play", "")
                            print(f"Com: playing **{song}** from youtube")
                            textTospeech(f"playing {song} from youtube")
                            pywhatkit.playonyt(song)
                    
                        #---------------Send Mail
                        elif "email" in reply:
                            print("Com: type the receiever email (before @)")
                            textTospeech("type the receiever email")
                            to = str(input("email: ").lower())+"@gmail.com"
                            sleep(1)
                            subject = speechTotext("what will be the subject of the email?")
                            body = speechTotext("what will be the message of the email?")
                            send_mail(subject, to, body)
                            sleep(3)
                            print("Com: the mail has been sent.")
                            textTospeech("the email has been sent")
                            
                        #---------------Exit
                        elif "goodbye, hope to see you soon" in reply:
                            textTospeech(reply)
                            exit()
                            
                        #---------------System Software
                        elif ""
                        
                            
                        #---------------Shutdown Device
                        elif "shutdown" in reply:
                            ch = speechTotext("are you sure?")
                            if "yes" or "right" or "definitely" in ch:
                                os.system("shutdown /s /t 10")
                                
                        elif reply is not None:
                            print(f"Com: {reply}")
                            textTospeech(reply)
                        
                break
            
            elif sentence == "":
                sentence = speechTotext("What do you want to say?")
                continue
            
            # checking probability    
            else:
                webbrowser.get().open(f"https://google.com/search?q={sentence}")
                break
        
        # checking face ID       
        else:
            textTospeech("Face does not match. Sorry.....")
            break
                
    
    
    
    