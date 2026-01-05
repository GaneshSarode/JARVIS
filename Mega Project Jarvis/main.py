import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import random
import musicLibrary
import games
import os
import google.generativeai as genai
# -------------------- GEMINI CONFIG --------------------

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------- SPEECH SETUP --------------------

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
        print(f"TTS Error: {e}")

# -------------------- AI RESPONSE --------------------

def get_ai_response(prompt):
    print("Calling Gemini...")
    speak("Just a moment while I look that up.")

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Sorry, I couldn't get an answer right now."


# -------------------- COMMAND HANDLING --------------------

def processCommand(command):
    c = command.lower()

    question_starters = (
        "tell me",
        "what is",
        "who is",
        "when did",
        "how does",
        "why is",
        "if"
    )

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "play guess the number" in c:
        games.guess_the_number_game(speak, recognizer)

    elif "play python quiz" in c:
        games.python_quiz_game(speak, recognizer)

    elif any(c.startswith(q) for q in question_starters):
        answer = get_ai_response(command)
        speak(answer)

    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1]
            link = musicLibrary.music.get(song)

            if link:
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak("I couldn't find that song in your library")

        except Exception:
            speak("Please say the song name again")

    else:
        speak("I did not recognize that command")

# -------------------- MAIN LOOP --------------------

if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            print("\nListening for wake word...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            wake_word = recognizer.recognize_google(audio)

            if wake_word.lower() == "jarvis":
                speak("Yes")
                print("Jarvis active")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Speech Recognition error:", e)
        except Exception as e:
            print("General error:", e)
