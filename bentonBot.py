import os
import time
import speech_recognition as sr
from gtts import gTTS
import requests
import time
import threading
from datetime import date


mUrl = "enterYourDiscordWebhookHere"


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            pass
    return said


def happyFunction(pressOnCount, happyCount, globalHappy, globalPress):
    text = get_audio().lower()
    wordTargets = ["press on", "happy days"]

    for word in wordTargets:
        if word in text:
            if word == "press on":
                pressOnCount += 1
                globalPress += 1
                updateStr = 'Daily press on count: ' + \
                    str(pressOnCount) + "\n" + \
                    "Total press on count: " + str(globalPress)
                data = {"content": updateStr}
                response = requests.post(mUrl, json=data)
            if word == "happy days":
                happyCount += 1
                globalHappy += 1
                updateStr = 'Daily happy days count: ' + \
                    str(happyCount) + "\n" + \
                    "Total happy days count: " + str(globalHappy)
                data = {"content": updateStr}
                response = requests.post(mUrl, json=data)

    return pressOnCount, happyCount, globalHappy, globalPress


def threadit(pressOnCount, happyCount, globalHappy, globalPress):
    pressOnCount, happyCount, globalHappy, globalPress = happyFunction(
        pressOnCount, happyCount, globalHappy, globalPress)
    threading.Timer(0.000000000000001, threadit, [
                    pressOnCount, happyCount, globalHappy, globalPress]).start()


if __name__ == "__main__":
    x = int(input("Enter the global Happy Days Count:\n"))
    y = int(input("Enter the global Press On Count:\n"))
    threadit(0, 0, x, y)
