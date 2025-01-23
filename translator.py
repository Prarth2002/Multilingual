import streamlit as st
from googletrans import Translator

# Initialize Translator
translator = Translator()

# Language options
languages = {
    'Afrikaans': 'af', 'Arabic': 'ar', 'Bangla': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg',
    'Chinese Simplified': 'zh-cn', 'Chinese Traditional': 'zh-tw', 'Croatian': 'hr',
    'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Estonian': 'et',
    'Filipino': 'tl', 'Finnish': 'fi', 'French': 'fr', 'German': 'de', 'Greek': 'el',
    'Gujarati': 'gu', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hungarian': 'hu', 'Indonesian': 'id',
    'Italian': 'it', 'Japanese': 'ja', 'Kannada': 'kn', 'Korean': 'ko', 'Malay': 'ms',
    'Malayalam': 'ml', 'Marathi': 'mr', 'Norwegian': 'no', 'Persian': 'fa', 'Polish': 'pl',
    'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Slovak': 'sk',
    'Slovenian': 'sl', 'Spanish': 'es', 'Swedish': 'sv', 'Tamil': 'ta', 'Telugu': 'te',
    'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Vietnamese': 'vi',
    'Welsh': 'cy'
}

# Streamlit App
st.title("Multilingual Natural Language Tool")

# Input text area
st.subheader("Input Text")
input_text = st.text_area("Paste or type your text here:")

# Language selection
st.subheader("Translation Options")
source_language = st.selectbox("Select Source Language:", ["Auto Detect"] + list(languages.keys()))
target_language = st.selectbox("Select Target Language:", list(languages.keys()))

# Translation button
if st.button("Translate"):
    if input_text.strip() == "":
        st.error("Please enter some text to translate.")
    else:
        try:
            # Determine source language
            src_lang_code = None if source_language == "Auto Detect" else languages[source_language]
            # Get target language code
            target_lang_code = languages[target_language]
            # Translate text
            translation = translator.translate(input_text, src=src_lang_code, dest=target_lang_code)
            # Display result
            st.subheader("Translated Text")
            st.write(translation.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("Built for literacy and learning in Indian education.")