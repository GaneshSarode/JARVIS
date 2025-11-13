import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import json
import requests
import random 
import musicLibrary 
import games 

API_KEY = "AIzaSyAmZVqfsy6BkL4SDKMod06POxURT74I4EI" 
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

recognizer = sr.Recognizer()

def speak(text):
    try:
        engine = pyttsx3.init() 
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate + 10) 
       
        engine.say(text)
        engine.runAndWait()
        engine.stop() 
    except Exception as e:
        print(f"ERROR: pyttsx3 failed to speak: {e}")

def get_ai_response(prompt):
    print("Calling API...")
    speak("Just a moment while I look that up.")
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {} }],
        "systemInstruction": {
            "parts": [{"text": "You are a helpful and concise voice assistant named Jarvis. Answer the user's query directly and briefly."}]
        }
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()      
        result = response.json()
        text = result.get('candidates')[0].get('content').get('parts')[0].get('text')
        return text
        
    except requests.exceptions.RequestException as e:
        print(f"AI API Request Error: {e}")
        return "I'm sorry, I couldn't connect to the knowledge base right now."
    except Exception:
        return "I received an empty or unreadable response from the knowledge base."


def processCommand(c):
    c_lower = c.lower()
    question_starters = [
        "tell me", 
        "what is", 
        "who is", 
        "when did", 
        "how does", 
        "why is",
        "if"
    ]
    if "open google" in c_lower:
        speak("opening google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c_lower:
        speak("opening youtube")
        webbrowser.open("https://youtube.com")

    elif "play guess the number" in c_lower:
        games.guess_the_number_game(speak, recognizer)
        
    elif "play python quiz" in c_lower:
        games.python_quiz_game(speak, recognizer)

    elif any(c_lower.startswith(starter) for starter in question_starters):
        
        query = c
        for starter in question_starters:
            if c_lower.startswith(starter):
                query = c[len(starter):].strip()
                if not query:
                    query = c
                break
            
        ai_response = get_ai_response(query)
        speak(ai_response)
    elif c_lower.startswith("play"):
        try:
            song = c.lower().split(" ", 1)[1] 
            link = musicLibrary.music.get(song)
            
            if link:
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find a song named {song} in your library.")
                
        except IndexError:
            speak("Please specify a song to play.")
        except Exception:
            speak("An error occurred while trying to play music.")
    else:
        speak("I did not recognize that command. You can try asking a question or asking to play a game.")


if __name__ == "__main__":
    speak("initializing jarvis....")
    
    while True:
        r = recognizer 
        print("\n# Listening for wake word...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2) 
                print("Say 'Jarvis' now...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3) 
                
            word = r.recognize_google(audio) 
            
            print(f"Recognized word: {word}")
            if word.lower() == "jarvis":
                speak("ya") 
                print("# Jarvis is active. Listening for command.")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.1) 
                    print("jarvis active... Speak your command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                command = r.recognize_google(audio)
                print(f"Command recognized: {command}")
                processCommand(command)
        except sr.UnknownValueError:
            pass 
        except sr.RequestError as e:
            print(f"Could not request results from Google SR service; check internet connection. Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")
