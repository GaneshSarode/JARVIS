import pyttsx3, time
e = pyttsx3.init()
print("pyttsx3 voices:", len(e.getProperty("voices")))
e.say("Ya")
e.runAndWait()
time.sleep(0.3)
print("TTS test done")
