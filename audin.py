import streamlit as st
import requests
import io
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
# Load environment variables from .env file
load_dotenv()
LLM="gemini-2.0-flash-exp"
# Get the API key from environment variables
subscription_key = os.getenv("SARVAM_SUBSCRIPTION_KEY")
xai_api_key = os.getenv("GEMINI_API_KEY") #gemini
sarvamurl = "https://api.sarvam.ai/text-to-speech"
sarvamheaders = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-subscription-key": subscription_key if subscription_key else ""
}
# Initialize OpenAI client
LLMclient=OpenAI(
  api_key=xai_api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# Function to send audio to Sarvam API for speech recognition
def transcribe_audio(audio_file, subscription_key, language_code='hi-IN'):
    url = "https://api.sarvam.ai/speech-to-text"
    # Prepare the payload with model and language code
    payload = {
        'model': 'saarika:v2',
        'language_code': language_code,
        'with_timesteps': 'false'
    }   
    # Prepare files for the request
    files = [
        ('file', ('audio.wav', audio_file, 'audio/wav'))
    ]   
    # Set headers including your API subscription key
    headers = {
        'api-subscription-key': subscription_key
    }   
    # Make the POST request to the API
    response = requests.post(url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        return response.json().get('transcript', 'No transcript available.')
    else:
        return f"Error: {response.status_code}, {response.text}"
# Function to process text using OpenAI API
def process_with_llm(text):
    try:
        response = LLMclient.chat.completions.create(
            model=LLM,
            messages=[
                {"role": "system", "content": "You are a samrt therapist who hepls people get over depression by talking to them as a friebd give them short and sooting answers which will help them feel better don't make the answers too long"},
                {"role": "user", "content": text}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"
# Language code mapping
language_mapping = {
    "English":"en-IN",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Odia": "od-IN",
    "Punjabi": "pa-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Gujarati": "gu-IN"
}
# Streamlit UI
st.title("Ashvin the Smart AI Therapist")
# Move language selection to sidebar
with st.sidebar:
    selected_language = st.selectbox("Select Language:", 
                                  list(language_mapping.keys()), 
                                  index=0)
    language_code = language_mapping[selected_language]
audio_value = st.audio_input("Record a voice message")
if audio_value:
    if subscription_key:
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(audio_value, subscription_key, language_code)
           # st.success("Transcription Complete:")
            st.write(f"User: {transcript}")
            # Change language code to Hindi if the selected language is English          
            # Process the transcript with OpenAI
            if xai_api_key:
                with st.spinner("Processing with Model..."):
                    model_response = process_with_llm(transcript)
                    #st.success("Model Processing Complete:")
                    st.write(f"Ashvin: {model_response}")
                    payload = {
                        "inputs": [model_response[:490]],
                        "target_language_code": language_code,
                        "speaker": "meera",
                        "pitch": 0.2,
                        "pace": 1.1,
                        "loudness": 0.8,
                        "enable_preprocessing": True,
                        "model": "bulbul:v1",
                        "speech_sample_rate": 8000
                    }
                    response = requests.request("POST", sarvamurl, json=payload, headers=sarvamheaders)
                    #print(response.json())
                    audio_data = response.json()
                    if "audios" in audio_data and audio_data["audios"]:
                        # Decode base64 audio
                        audio_bytes = base64.b64decode(audio_data["audios"][0])
                        # Play the audio in Streamlit
                        st.audio(audio_bytes, format="audio/wav", autoplay=True)
            else:
                st.error(" API Key not found in environment variables.")
    else:
        st.error("API Subscription Key not found in environment variables.")