import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import json
import requests
import random # Needed for games

# Assuming you have a file named musicLibrary.py with a music dictionary
import musicLibrary 
# --- NEW: Import the games library
import games 

# --- CRITICAL: GEMINI API SETUP ---
# NOTE: Replace "" with your actual Gemini API Key...
API_KEY = "YOUR_ACTUAL_API_KEY_GOES_HERE" # Assuming you put your key here
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

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
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate + 50) 
        # --------------------------
        
        engine.say(text)
        engine.runAndWait()
        engine.stop() # Stop the engine after speaking to release resources
    except Exception as e:
        print(f"ERROR: pyttsx3 failed to speak: {e}")

def get_ai_response(prompt):
    """Function to call the Gemini API and get a text response."""
    print("Calling Gemini API...")
    speak("Just a moment while I look that up.")
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {} }], # Enable search grounding for real-time info
        "systemInstruction": {
            "parts": [{"text": "You are a helpful and concise voice assistant named Jarvis. Answer the user's query directly and briefly."}]
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        # Use requests for synchronous API call
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise exception for bad status codes
        
        result = response.json()
        text = result.get('candidates')[0].get('content').get('parts')[0].get('text')
        return text
        
    except requests.exceptions.RequestException as e:
        print(f"AI API Request Error: {e}")
        return "I'm sorry, I couldn't connect to the knowledge base right now."
    except Exception:
        return "I received an empty or unreadable response from the knowledge base."


def processCommand(c):
    """Handles and executes the commands recognized after the wake word."""
    c_lower = c.lower()
    
    # Define a list of common question starting phrases
    question_starters = [
        "tell me", 
        "what is", 
        "who is", 
        "when did", 
        "how does", 
        "why is"
    ]
    
    # Command 1: Open Google
    if "open google" in c_lower:
        speak("opening google")
        webbrowser.open("https://google.com")
        
    # Command 2: Open YouTube
    elif "open youtube" in c_lower:
        speak("opening youtube")
        webbrowser.open("https://youtube.com")

    # --- NEW: Game Commands ---
    elif "play guess the number" in c_lower:
        # Pass the current speak and recognizer functions to the game
        games.guess_the_number_game(speak, recognizer)
        
    elif "play python quiz" in c_lower:
        # Pass the current speak and recognizer functions to the game
        games.python_quiz_game(speak, recognizer)
    # --- END NEW: Game Commands ---

    # Command 3: AI Query / General Knowledge
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
        
    # Command 4: Play music (Now the final part of the 'play' logic)
    elif c_lower.startswith("play"):
        try:
            # Note: This is now only for music, as game commands are handled above
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
    
    # Command 5: Default/Unknown Command
    else:
        speak("I did not recognize that command. You can try asking a question or asking to play a game.")


if __name__ == "__main__":
    speak("initializing jarvis....")
    
    while True:
        # --- PHASE 1: LISTEN FOR WAKE WORD ("jarvis") ---
        r = recognizer 
        print("\n# Listening for wake word...")
        
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2) 
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
