import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize the mixer module
    pygame.mixer.init()

    # Load and play the MP3 file
    pygame.mixer.music.load("temp.mp3")
    #play the mp3 file
    pygame.mixer.music.play()

    # Keep the program running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')



def aiProcess(command):
    openai.api_key = "your api key"

    # Using the latest chat model for completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ],
        max_tokens=100,
        temperature=0.5,
    )

    # Extract and return the assistant's response text
    return response.choices[0].message['content'].strip()

def processCommand(c):
    if 'open google' in c.lower():
        webbrowser.open("https://google.com")
    elif 'open youtube' in c.lower():
        webbrowser.open("https://youtube.com")
    elif 'open linkedin' in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith('play'):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    else:
        #let open ai handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == '__main__':
    speak("Initializing Leo...")
    while True:
        # listen for the wake word jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=='leo'):
                speak('Yes')
                #listen for command
                with sr.Microphone() as source:
                    print("Leo Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print('Error; {0}',format(e))
