import speech_recognition as sr
import pyttsx3
import time
import webbrowser
# Assuming you have a file named musicLibrary.py with a music dictionary
import musicLibrary 
import requests

# Initialize the speech recognition globally
recognizer = sr.Recognizer()

def speak(text):
    """
    Function to make Jarvis speak the given text.
    Optimized: Initializes the engine inside the function for reliability,
    and sets the rate for faster speech.
    """
    try:
        # Re-initialize the engine for every speak call
        engine = pyttsx3.init() 
        
        # --- SPEED OPTIMIZATION ---
        # Get current rate and increase it (e.g., from 150 to 200 wpm)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate + 50) 
        # --------------------------
        
        engine.say(text)
        engine.runAndWait()
        engine.stop() # Stop the engine after speaking to release resources
    except Exception as e:
        print(f"ERROR: pyttsx3 failed to speak: {e}")

def processCommand(c):
    """Handles and executes the commands recognized after the wake word."""
    # Command 1: Open Google
    if "open google" in c.lower():
        speak("opening google")
        webbrowser.open("https://google.com")
        
    # Command 2: Open YouTube
    elif "open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com")
        
    # Command 3: Play music
    elif c.lower().startswith("play"):
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
    # elif "news" in c.lower():

    #     r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=API_KEY")
    #     if r.status_code != 200:

    #         print("Error:", r.status_code, r.text)
    #     else:
    # # Convert JSON r into Python dict
    #         data = r.json()

    # # Extract and print the headlines
    #         print("\nTop Headlines:\n")
    # for i, article in enumerate(data.get("articles", []), start=1):
    #     speak(f"{i}. {article.get('title')}")      
if __name__ == "__main__":
    speak("initializing jarvis....")
    
    while True:
        # --- PHASE 1: LISTEN FOR WAKE WORD ("jarvis") ---
        r = recognizer 
        print("\n# Listening for wake word...")
        
        try:
            with sr.Microphone() as source:
                # --- SPEED OPTIMIZATION ---
                # Reduce noise adjustment time from 0.5 to 0.2 seconds
                r.adjust_for_ambient_noise(source, duration=0.2) 
                # --------------------------
                
                print("Say 'Jarvis' now...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3) 
                
            word = r.recognize_google(audio) 
            
            print(f"Recognized word: {word}")
            
            # Check if the recognized word is the wake word
            if word.lower() == "jarvis":
                speak("ya") 
                
                # --- PHASE 2: LISTEN FOR COMMAND ---
                print("# Jarvis is active. Listening for command.")
                with sr.Microphone() as source:
                    # Give it a quick adjustment for the command phrase
                    r.adjust_for_ambient_noise(source, duration=0.1) 
                    print("jarvis active... Speak your command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    
                command = r.recognize_google(audio)
                print(f"Command recognized: {command}")
                
                # Execute the command
                processCommand(command)

        except sr.UnknownValueError:
            pass 
        except sr.RequestError as e:
            print(f"Could not request results from Google SR service; check internet connection. Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")