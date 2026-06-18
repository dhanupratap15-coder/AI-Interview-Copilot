
from Generate_Question import genrate_question
import re
import speech_recognition as sr
from gtts import gTTS
import tempfile
import pygame
import os
import time
from ChatModel import mistral_chat_modle
llm= mistral_chat_modle.llm
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()


# -------------------------
# Setup
# -------------------------

recognizer = sr.Recognizer()
recognizer.pause_threshold = 2

questions = genrate_question.generate_questions()

question_list = questions.split("\n")

qust = [
    re.sub(r'^\d+\.\s*', '', q)
    for q in question_list
    if q.strip()
]

data = {}

pygame.mixer.init()

# -------------------------
# Speak Function
# -------------------------

def speak(text):

    try:

        tts = gTTS(text=text, lang="en")

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as fp:

            temp_file = fp.name

        tts.save(temp_file)

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()

        time.sleep(0.5)

        os.remove(temp_file)

    except Exception as e:

        print("Speech Error:", e)

# -------------------------
# Welcome Message
# -------------------------

name = input("What is your good name : ")

welcome = (
    f"Welcome {name}. "
    f"We are starting your interview. "
    f"First of all tell me about yourself."
)

print("\n" + welcome)

speak(welcome)

# -------------------------
# Introduction
# -------------------------


try:

    with sr.Microphone() as source:

        print("\nListening Introduction...\n")

        recognizer.adjust_for_ambient_noise(
            source
        )

        audio = recognizer.listen(
    source,
    timeout=5,
    phrase_time_limit=60
)

    intro = recognizer.recognize_google(audio)

    print("\nYour Introduction:")
    print(intro)

    data["Introduction"] = intro

except sr.UnknownValueError:

    print("Could not understand audio")

    data["Introduction"] = ""

except sr.RequestError as e:

    print("Error:", e)

    data["Introduction"] = ""

# -------------------------
# Question Round
# -------------------------

for question in qust:

    print("\n" + "=" * 60)
    print("Question:")
    print(question)
    print("=" * 60)

    speak(question)

    try:

        with sr.Microphone() as source:

            print("\nListening Answer...\n")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(source)

        answer = recognizer.recognize_google(audio)

        print("\nYour Answer:")
        print(answer)

        data[question] = answer

    except sr.UnknownValueError:

        print("Could not understand audio")

        data[question] = ""

    except sr.RequestError as e:

        print("Error:", e)

        data[question] = ""

# -------------------------
# Close Mixer
# -------------------------

pygame.mixer.quit()


print("\nInterview Completed Successfully.")
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
        (
            "system",'''
           You are an expert interview evaluator.

You will receive a Python dictionary where:

* Key = Interview Question
* Value = Student Answer

For each question:

* Analyze the answer.
* Identify mistakes, missing points, and areas for improvement.
* Give a rating out of 10.
* Briefly explain why that rating was given.

Finally provide:

* Overall Interview Rating (out of 10)
* Student's strengths
* Student's weaknesses
* Topics the student should improve

Be concise, accurate, and professional.

'''
        ),
        (
            "human",
            """
            data:
            {data}"""
        )
    ])
try:
    chain = prompt | llm | parser

    review = chain.invoke({
                "data": data
                
            })
except KeyError as e:
    print(f"Missing input variable: {e}")

except AttributeError as e:
    print(f"Attribute Error: {e}")
    print("Check if 'resumeroll.resume' exists.")

except Exception as e:
    print(f"An error occurred: {e}")         
print(review)