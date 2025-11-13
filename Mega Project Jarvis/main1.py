import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import musicLibrary 

# NOTE: We are removing the global initialization here:
# recognizer = sr.Recognizer()
# engine = pyttsx3.init()
# And moving the initialization inside the speak function for better reliability
# Initialize the speech recognition globally (this is fine)
recognizer = sr.Recognizer()

def speak(text):
    """
    Function to make Jarvis speak the given text.
    CRITICAL FIX: Initializes the engine inside the function to prevent silent
    failures due to engine lock-up or improper initialization queueing.
    """
    try:
        # Re-initialize the engine for every speak call
        engine = pyttsx3.init() 
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

if __name__ == "__main__":
    speak("initializing jarvis....")
    
    # We removed the time.sleep(1) because the re-initialization inside speak()
    # handles the queuing issue better.
    
    while True:
        # --- PHASE 1: LISTEN FOR WAKE WORD ("jarvis") ---
        r = recognizer # Use the globally initialized recognizer
        print("\n# Listening for wake word...")
        
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5) 
                print("Say 'Jarvis' now...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3) 
                
            word = r.recognize_google(audio) 
            
            # --- DEBUGGING STEP ---
            print(f"Recognized word: {word}")
            # ----------------------
            
            # Check if the recognized word is the wake word
            if word.lower() == "jarvis":
                # This is the line we want to hear!
                speak("ya") 
                
                # --- PHASE 2: LISTEN FOR COMMAND ---
                print("# Jarvis is active. Listening for command.")
                with sr.Microphone() as source:
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
