import random
import speech_recognition as sr
import time

def guess_the_number_game(speak, recognizer):
    """
    Plays the 'Guess the Number' game using voice input.
    The game takes over the main microphone loop temporarily.
    """
    speak("Starting Guess the Number. I'm thinking of a number between 1 and 10.")
    speak("You have 5 tries. What is your first guess?")
    
    # Generate a random number between 1 and 10
    secret_number = random.randint(1, 10)
    max_tries = 5
    
    for guess_count in range(1, max_tries + 1):
        try:
            r = recognizer
            with sr.Microphone() as source:
                # Optimized: Very fast noise adjustment
                r.adjust_for_ambient_noise(source, duration=0.05)
                # Increased listening time for better single-word recognition
                audio = r.listen(source, timeout=5, phrase_time_limit=3) 
                
            # Recognize the guess as text
            guess_text = r.recognize_google(audio)
            print(f"User guessed: {guess_text}")
            
            # Try to convert the recognized text to an integer
            try:
                # Common issue: recognizing "two" as 2, etc.
                # Added 'one' to 1 conversion
                processed_guess = guess_text.strip().lower().replace(" ", "")
                processed_guess = processed_guess.replace("one", "1").replace("two", "2").replace("to", "2")
                processed_guess = processed_guess.replace("three", "3").replace("for", "4").replace("four", "4")
                processed_guess = processed_guess.replace("five", "5").replace("six", "6").replace("seven", "7")
                processed_guess = processed_guess.replace("eight", "8").replace("nine", "9").replace("ten", "10")

                guess = int(processed_guess)
            except ValueError:
                speak("I didn't hear a number. Please say a number between 1 and 10 clearly.")
                continue

            if guess == secret_number:
                speak(f"You got it! The number was {secret_number}. You won in {guess_count} tries!")
                return # End the game
            elif guess < secret_number:
                speak("Too low.")
            else:
                speak("Too high.")
                
            remaining = max_tries - guess_count
            if remaining > 0:
                speak(f"Try again. You have {remaining} tries left.")
            
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
        except sr.WaitTimeoutError:
            speak("You took too long. I'll wait a little longer.")
        except Exception as e:
            print(f"Game error: {e}")
            speak("An unexpected error occurred in the game.")
            
    # If the loop finishes without a correct guess
    speak(f"Game over! You ran out of tries. The secret number was {secret_number}.")


def python_quiz_game(speak, recognizer):
    """
    Plays a short Python Quiz using voice input.
    """
    questions = [
        {"q": "What keyword is used to define a function in Python?", "a": "def"},
        {"q": "Which data type is ordered, mutable, and allows duplicate members?", "a": "list"},
        {"q": "What command displays output to the console?", "a": "print"},
        {"q": "What is the result of 5 double star 2?", "a": "25"}
    ]
    
    speak("Starting the Python Quiz! Answer with a single word or short phrase. Let's begin.")
    score = 0
    
    for i, item in enumerate(questions):
        speak(f"Question {i + 1}. {item['q']}")
        time.sleep(0.5) # Pause to give the user time to listen

        try:
            r = recognizer
            with sr.Microphone() as source:
                # Optimized: Very fast noise adjustment
                r.adjust_for_ambient_noise(source, duration=0.05)
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                
            user_answer = r.recognize_google(audio).lower().strip()
            print(f"User answer: {user_answer}")

            correct_answer = item['a'].lower().strip()
            
            # Use fuzzy matching for short answers
            if user_answer in correct_answer or correct_answer in user_answer:
                score += 1
                speak("That is correct!")
            else:
                speak(f"Incorrect. The answer was {item['a']}.")
                
        except sr.UnknownValueError:
            speak("I couldn't understand your answer. Moving on.")
        except sr.WaitTimeoutError:
            speak("Time's up! Moving on.")
        except Exception as e:
            print(f"Quiz error: {e}")
            speak("An unexpected error occurred during the quiz.")
            
    speak(f"The quiz is over! Your final score is {score} out of {len(questions)}.")