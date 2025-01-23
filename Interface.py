import streamlit as st
from googletrans import Translator, LANGUAGES
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import speech_recognition as sr  # Import speech recognition module
import time
import requests

# Initialize Translator and TTS Engine
translator = Translator()
tts_engine = pyttsx3.init()

# List of Indian languages and English available in Google Translate
indian_languages = {
    'English': 'en',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Urdu': 'ur',
    'Gujarati': 'gu',
    'Malayalam': 'ml',
    'Kannada': 'kn',
    'Oriya': 'or',
    'Punjabi': 'pa',
    'Sindhi': 'sd',
    'Nepali': 'ne',
    'Arabic': 'ar',
    'Portuguese': 'pt'
}

# Function to set TTS voice
def set_tts_voice(lang_code):
    for voice in tts_engine.getProperty('voices'):
        if lang_code.lower() in voice.languages:
            tts_engine.setProperty('voice', voice.id)
            return True
    return False

# Function to speak text
def speak_text(text, lang_code):
    try:
        # Use pyttsx3 if the language is supported
        if set_tts_voice(lang_code):
            tts_engine.say(text)
            tts_engine.runAndWait()
        else:
            # Use gTTS for unsupported languages
            tts = gTTS(text=text, lang=lang_code)
            tts.save("temp.mp3")
            audio = AudioSegment.from_file("temp.mp3", format="mp3")
            play(audio)
            os.remove("temp.mp3")
    except Exception as e:
        st.error(f"Error during speech synthesis: {e}")

# Function to recognize speech with improved sensitivity and timeout
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Adjust microphone sensitivity for ambient noise
    with mic as source:
        st.info("Listening for speech... Please speak clearly.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Listen for a longer period

    try:
        # Use Google Web Speech API for recognition (Improved for English)
        text = recognizer.recognize_google(audio, language='en-US')  # Specify English explicitly
        st.session_state.input_text = text
        st.success(f"Recognized Text: {text}")
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the speech. Please try again.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")

# Initialize session state for input and translated text
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# Streamlit App
st.set_page_config(layout="wide")

# Set the background image (using a URL)
background_url = "https://github.com/Prarth2002/IMG/blob/main/pastel-blue.jpg?raw=true"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({background_url});
        background-size: cover;
        background-position: center center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
with st.sidebar:
    st.markdown("**Multilingual Natural Language Tool**")
    st.markdown("Support literacy and learning in Indian education")
    st.image("https://github.com/Prarth2002/Images/blob/main/multilingual-removebg-preview.png?raw=true", use_column_width=True)
    # Add an "About" option in the sidebar
    about_option = st.radio("Navigation", ["Home", "About"])

# Display content based on selected option
if about_option == "About":
    st.title("About the Multilingual Natural Language Tool")
    
    # Fetch the content from the text file URL
    text_file_url = "https://github.com/Prarth2002/IMG/blob/main/Text%201.txt?raw=true"
    response = requests.get(text_file_url)
    about_text = response.text  # Get the text content of the file
    
    # Display the information under the About section
    st.subheader("Purpose and Vision")
    st.markdown(about_text)

# Main content
if about_option == "Home":
    st.title("Multilingual Natural Language Tool")

    # Speech-to-text button
    if st.button("🎙️ Listen to Speech and Convert to Text"):
        # Show sound wave animation while listening
        with st.spinner("Listening..."):
            # Add a simple animation using a text indicator or you can use a gif
            st.markdown(
                """
                <div style="font-size:30px; color:white; text-align:center;">
                    🔊🎶 Listening... 🎶🔊
                </div>
                """,
                unsafe_allow_html=True
            )
            recognize_speech()

    # Input text area
    st.subheader("Input Text")
    st.session_state.input_text = st.text_area(
        "Paste or type your text here:", value=st.session_state.input_text
    )

    # Language selection
    st.subheader("Translation Options")
    source_language = st.selectbox("Select Source Language:", ["Auto Detect"] + list(indian_languages.keys()))
    target_language = st.selectbox("Select Target Language:", list(indian_languages.keys()))

    # Translation button
    if st.button("Translate"):
        if not st.session_state.input_text.strip():
            st.error("Please enter some text to translate.")
        else:
            try:
                # Get the source language code
                src_lang_code = None if source_language == "Auto Detect" else indian_languages[source_language]
                # Get the target language code
                target_lang_code = indian_languages[target_language]
                # Perform translation
                translation = translator.translate(st.session_state.input_text, src=src_lang_code, dest=target_lang_code)
                # Store translated text in session state
                st.session_state.translated_text = translation.text
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Display translated text if available
    if st.session_state.translated_text:
        st.subheader("Translated Text")
        st.write(st.session_state.translated_text)

        # Buttons for speaking the translated text
        col1, col2, col3 = st.columns(3)

        # Speak translated text
        if col1.button("🔊 Speak"):
            with st.spinner("Speaking..."):
                speak_text(st.session_state.translated_text, indian_languages[target_language])

        # Stop speaking
        if col2.button("⛔ Stop"):
            tts_engine.stop()
            st.success("Stopped speaking.")

        # Speak again
        if col3.button("🔁 Speak Again"):
            with st.spinner("Speaking again..."):
                speak_text(st.session_state.translated_text, indian_languages[target_language])

# Footer
st.markdown("---")
st.markdown("Built for literacy and learning in Indian education.")
