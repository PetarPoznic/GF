import streamlit as st
import pandas as pd
from langdetect import detect, lang_detect_exception
from googletrans import Translator, LANGUAGES

st.title("Language Detection and Translation App")

# Function to detect language
def detect_language(text):
    try:
        if not text:
            return None  # or 'empty' or any other representation of your choice
        lang = detect(text)
        if lang in LANGUAGES:
            return LANGUAGES[lang]
        return lang
    except lang_detect_exception.LangDetectException:
        return 'unknown'

# Function to translate text to English
def translate_to_english(text, translator):
    try:
        if not text:
            return text  # keep it empty
        return translator.translate(text, dest='en').text
    except Exception as e:
        return text

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("File uploaded successfully!")

    # Display columns
    st.write("Columns in the file:")
    st.write(df.columns.tolist())

    # Select columns for translation
    selected_columns = st.multiselect("Select columns to translate", df.columns.tolist())

    if selected_columns:
        translator = Translator()

        for column in selected_columns:
            df[f"{column}_language"] = df[column].apply(detect_language)
            df[f"{column}_translated"] = df[column].apply(lambda x: translate_to_english(x, translator))

        st.write("Translation completed!")

        # Display the dataframe
        st.write(df.head())

        # Download the modified dataframe
        @st.cache
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download Translated Data as CSV",
            data=csv,
            file_name='translated_data.csv',
            mime='text/csv',
        )
