import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import openai
import os
from gtts import gTTS
import pygame
import musicLibrary
from config import OPENAI_API_KEY, NEWS_API_KEY

# Initialize
engine = pyttsx3.init()
recognizer = sr.Recognizer()
openai.api_key = OPENAI_API_KEY

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

def open_website(command):
    sites = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "linkedin": "https://linkedin.com",
        "facebook": "https://facebook.com"
    }
    for site in sites:
        if site in command:
            webbrowser.open(sites[site])
            speak(f"Opening {site}")
            return True
    return False

def play_music():
    song = musicLibrary.get_song()
    webbrowser.open(song)
    speak("Playing music...")

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    if articles:
        for i, article in enumerate(articles[:5]):
            speak(article["title"])
    else:
        speak("Sorry, I couldn't fetch the news right now.")

def ask_openai(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content":query}]
    )
    answer = response["choices"][0]["message"]["content"]
    speak(answer)

def main():
    speak("Initializing Jarvis...")
    while True:
        command = listen()
        if "jarvis" in command:
            speak("Ya, I am listening.")
            command = listen()

            if "open" in command:
                if not open_website(command):
                    speak("Website not found.")

            elif "play music" in command:
                play_music()

            elif "news" in command:
                fetch_news()

            elif "stop" in command or "exit" in command:
                speak("Goodbye!")
                break

            else:
                ask_openai(command)

if __name__ == "__main__":
    main()
