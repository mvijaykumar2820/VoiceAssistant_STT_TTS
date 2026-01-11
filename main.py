import speech_recognition as sr
from groq import Groq
import os
import pyttsx3
import time



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

r = sr.Recognizer()
r.pause_threshold = 0.8
r.energy_threshold = 300

# import and set up Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("Listening... Say bye to stop.")

while True:
    try:
        print("Speak now...")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio = r.listen(source, phrase_time_limit=5)

        result = r.recognize_whisper(audio, model="base").strip()
        print("Heard:", result)

        # Ignore silence / noise / garbage
        if len(result) < 3:
            print("Ignored: too short")
            continue

        if result.lower() in ["uh", "um", "hmm", "huh", ""]:
            print("Ignored: filler noise")
            continue

        if "bye" in result.lower() or "stop" in result.lower():
            speak("Goodbye")
            break

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": ("you are my robot i made you to help me with simple tasks and have funhort and simple convo with me my name is vijay"
                    ),
                },
                {
                    "role": "user",
                    "content": result,
                },
            ],
            temperature=0.2,
        )

        reply = completion.choices[0].message.content.strip()
        print("AI:", reply)

        speak(reply)
        time.sleep(0.7)

    except sr.UnknownValueError:
        print("Didn't understand, try again.")
    except Exception as e:
        print("Error:", e)
