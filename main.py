import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from bs4 import BeautifulSoup
import requests
import psutil

from google.auth.transport import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 125)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            comand = listener.recognize_google(voice)
            comand = comand.lower()
            if 'alex' in comand:
                comand = comand.replace('alex', '')
    except:
        pass
    return comand

def battery_status():
    battery = psutil.sensors_battery()
    talk(f"Battery is at {battery.percent} percent.")

import os
from docx import Document
import PyPDF2

def read_any_file(file_name):
    try:
        file_ext = os.path.splitext(file_name)[1].lower()

        if file_ext == '.txt':
            with open(file_name, "r") as file:
                content = file.read()
                talk(f"Here is the content of {file_name}")
                talk(content)

        elif file_ext == '.docx':
            doc = Document(file_name)
            full_text = [para.text for para in doc.paragraphs]
            content = "\n".join(full_text)
            talk(f"Here is the content of {file_name}")
            talk(content)

        elif file_ext == '.pdf':
            with open(file_name, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                talk(f"Here is the content of {file_name}")
                talk(text)

        else:
            talk(f"Sorry, I don't support reading {file_ext} files yet.")

    except FileNotFoundError:
        talk(f"Sorry, I couldn't find the file named {file_name}")
    except Exception as e:
        talk(f"An error occurred while reading the file: {str(e)}")
        
def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif "battery" in command:
         battery_status()
    elif "read file" in command:
    words = command.split()
    for word in words:
        if word.endswith(".txt") or word.endswith(".pdf") or word.endswith(".docx"):
            read_any_file(word)
            break
        else:
        talk("Please specify a valid file name like notes.txt or report.pdf.")
    else:
        talk('Please say the command again.')


run_alexa()
