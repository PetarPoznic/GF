import streamlit as st
import pandas as pd
from langdetect import detect, lang_detect_exception
from googletrans import Translator

st.title("Language Detection and Translation App")

# Function to detect language
def detect_language(text):
    try:
        return detect(text)
    except lang_detect_exception.LangDetectException:
        return 'unknown'

# Function to translate text to English
def translate_text(text, translator):
    if text:
        try:
            translated = translator.translate(text, dest='en')
            return translated.text
        except Exception as e:
            return text
    return ''

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
            df[f"{column}_lang"] = df[column].apply(lambda x: detect_language(str(x)) if pd.notnull(x) else '')
            df[f"{column}_translated"] = df[column].apply(lambda x: translate_text(str(x), translator) if pd.notnull(x) else '')

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
