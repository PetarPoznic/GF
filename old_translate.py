import pandas as pd
from langdetect import detect
from googletrans import Translator, LANGUAGES
import os
import numpy as np

pd.set_option('display.max_columns', 500)

# Sample data
data = {
    'name': ['John', 'Maria', 'Alex', 'Linda'],
    'answer_1': ['Hello', 'Hola', '', 'Bonjour'],
    'answer_2': ['How are you?', '¿Cómo estás?', 'Comment ça va?', '']
}

df = pd.DataFrame(data)

def detect_language(text):
    try:
        if not text:
            return None  # or 'empty' or any other representation of your choice
        lang = detect(text)
        if lang in LANGUAGES:
            return LANGUAGES[lang]
        return lang
    except:
        return 'unknown'

translator = Translator()

def translate_to_english(text):
    try:
        if not text:
            return text  # keep it empty
        return translator.translate(text, dest='en').text
    except:
        return text

# Detect language and translate answer_1
df['answer_1_language'] = df['answer_1'].apply(detect_language)
df['answer_1_translated'] = df['answer_1'].apply(translate_to_english)

# Detect language and translate answer_2
df['answer_2_language'] = df['answer_2'].apply(detect_language)
df['answer_2_translated'] = df['answer_2'].apply(translate_to_english)

print(df)
