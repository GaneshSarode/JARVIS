import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary
import os
import google.cloud 
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
def processCommand(c):              
            if "open google" in c.lower():
                webbrowser.open("https://google.com")
            elif  "open google" in c.lower():
                webbrowser.open("https://youtube.com")
            elif c.lower().startswith("play"):
                song = c.lower().split(" ")[1]
                link = musicLibrary.music[song]
                webbrowser.open(link)
                musicLibrary.music[song]
  
if __name__ == "__main__":
    speak("initializing jarvis.....")
    while True: 
            # listen for the wake word "jarvis"
            # obtain audio from the microphone
        r = sr.Recognizer()
        
        
        # recognize speech using Sphinx
        print("recognizing...")
        try:
           with sr.Microphone() as source:

            print("Listening...")
            audio = r.listen(source)    
           word = r.recognize_google(audio)

           if(word.lower() == "jarvis"):
              speak("Ya")          
              # Listen for command
              with sr.Microphone() as source:
                print("jarvis active...")
                audio = r.listen(source)
                command = r.recognize_google(audio)

                processCommand(command)
                   
        except Exception as e:
            print("Error; {0}".format(e))
