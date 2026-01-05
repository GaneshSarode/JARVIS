# JARVIS – Voice Assistant Using Python & API

## Overview

JARVIS is a Python-based voice assistant that listens for a wake word (“Jarvis”) and performs actions such as answering general knowledge questions using Google’s Gemini AI, opening websites, playing music, and running interactive games. The project integrates speech recognition, text-to-speech, and generative AI to demonstrate real-time voice-driven interaction.

This project is intended for learning, experimentation, and demonstration purposes.

---

## Features

- Wake-word detection (“Jarvis”)
- Speech-to-text using microphone input
- AI-powered question answering using Gemini 2.5 Flash
- Text-to-speech voice responses
- Open Google and YouTube via voice commands
- Play songs from a local music library
- Voice-controlled mini-games:
  - Guess the Number
  - Python Quiz

---
## Technologies Used

- Python 3
- SpeechRecognition (speech-to-text)
- pyttsx3 (text-to-speech)
- Google Generative AI SDK (Gemini)
- Web browser automation
- Microphone-based audio input

---

## Working Principle

The system continuously monitors audio input for the wake word “Jarvis.” Upon detection, it enters an active listening state and records the user’s spoken command. The command is converted to text and analyzed. If it matches predefined actions such as opening websites, playing music, or launching games, the corresponding function is executed. For general or informational queries, the text is passed to Gemini AI, and the generated response is spoken aloud. After execution, the system returns to its idle listening state.

---

## Limitations

This assistant requires an active internet connection for AI-based responses. It is designed for single-user, local execution and does not include authentication, user profiles, or persistent conversational memory. Speech recognition accuracy depends on microphone quality and surrounding noise. The project is not intended for production environments or security-critical applications.

---

## Future Improvements

Future enhancements may include conversational memory, improved natural language command understanding, a graphical user interface, offline fallback responses, and integration with additional services such as weather updates, reminders, or calendar management.

---

## Security Considerations

Sensitive credentials such as API keys are handled securely using environment variables and are never hardcoded or committed to version control. This approach follows standard secure development practices and prevents accidental exposure of secrets.

---

## Author

**Ganesh Sarode**



## Overview

JARVIS is a Python-based voice assistant that listens for a wake word (“Jarvis”) and performs actions such as answering general knowledge questions using Google’s Gemini AI, opening websites, playing music, and running interactive games. The project integrates speech recognition, text-to-speech, and generative AI to demonstrate real-time voice-driven interaction.

This project is intended for learning, experimentation, and demonstration purposes.

---

## Features

- Wake-word detection (“Jarvis”)
- Speech-to-text using microphone input
- AI-powered question answering using Gemini 2.5 Flash
- Text-to-speech voice responses
- Open Google and YouTube via voice commands
- Play songs from a local music library
- Voice-controlled mini-games:
  - Guess the Number
  - Python Quiz

---
## Technologies Used

- Python 3
- SpeechRecognition (speech-to-text)
- pyttsx3 (text-to-speech)
- Google Generative AI SDK (Gemini)
- Web browser automation
- Microphone-based audio input

---

## Working Principle

The system continuously monitors audio input for the wake word “Jarvis.” Upon detection, it enters an active listening state and records the user’s spoken command. The command is converted to text and analyzed. If it matches predefined actions such as opening websites, playing music, or launching games, the corresponding function is executed. For general or informational queries, the text is passed to Gemini AI, and the generated response is spoken aloud. After execution, the system returns to its idle listening state.

---

## Limitations

This assistant requires an active internet connection for AI-based responses. It is designed for single-user, local execution and does not include authentication, user profiles, or persistent conversational memory. Speech recognition accuracy depends on microphone quality and surrounding noise. The project is not intended for production environments or security-critical applications.

---

## Future Improvements

Future enhancements may include conversational memory, improved natural language command understanding, a graphical user interface, offline fallback responses, and integration with additional services such as weather updates, reminders, or calendar management.

---

## Security Considerations

Sensitive credentials such as API keys are handled securely using environment variables and are never hardcoded or committed to version control. This approach follows standard secure development practices and prevents accidental exposure of secrets.

---

## Author

**Ganesh Sarode**

