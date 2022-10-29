import sys
from tkinter import Tk, Canvas, PhotoImage, mainloop

import pyttsx3 as tts
import speech_recognition
from neuralintents import GenericAssistant

window = Tk()
window.title("AI Chat Bot")
window.config(padx=100, pady=50)

speaker = tts.init()
speaker.setProperty('rate', 150)
speaker.say("Welcome to the Data Laboratory, How can I help you?")
speaker.runAndWait()

canvas = Canvas(width=512, height=512,highlightthickness=0)
tomato_img = PhotoImage(file="pngwing.png")
canvas.create_image(256,256,image=tomato_img)
canvas.grid(column=1, row=1)



mainloop()



recognizer = speech_recognition.Recognizer()



todo_list = ['Go shopping', 'clean room', 'record video']


def create_note():
    global recognizer

    speaker.say("what do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

                with open(f"{filename}.txt", 'w') as f:
                    f.write(note)
                    done = True
                    speaker.say(f"I successfully created the not {filename}")
                    speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you")
            speaker.runAndWait()


def add_todo():
    global recognizer
    speaker.say("What todo do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say("I added {item} to the list")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand")
            speaker.runAndWait()


def show_todos():
    speaker.say("The items on your list are")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Welcome to the Data Laboratory, How can I help you?")
    speaker.runAndWait()


def quit():
    speaker.say("bye")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todo": show_todos,
    "quit": quit
}
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()
        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()



