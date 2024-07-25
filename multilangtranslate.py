import streamlit as st
import pandas as pd
from langdetect import detect, lang_detect_exception
from googletrans import Translator, LANGUAGES
from io import BytesIO

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
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        return f"Error: {str(e)}"

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'])

if uploaded_file:
    # Read file
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
        @st.cache_data
        def convert_df_to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.close()
            processed_data = output.getvalue()
            return processed_data

        excel_data = convert_df_to_excel(df)

        st.download_button(
            label="Download Translated Data as Excel",
            data=excel_data,
            file_name='translated_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
