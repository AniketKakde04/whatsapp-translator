import os
import requests
from urllib.parse import urlparse
from google import genai

# Gemini client uses API key from environment
client = genai.Client()

def is_supported_audio(media_url):
    if not media_url:
        return False
    path = urlparse(media_url).path
    return path.endswith(".mp3") or path.endswith(".wav")

def transcribe_and_translate(media_url):
    file_name = "audio.mp3"  # Works for .wav too

    try:
        print("Downloading audio from:", media_url)
        response = requests.get(media_url)
        with open(file_name, "wb") as f:
            f.write(response.content)

        print("Uploading to Gemini...")
        uploaded = client.files.upload(file=file_name)

        prompt = (
            "Transcribe and translate this audio file:\n"
            "1. Show the transcription in the original language.\n"
            "2. Provide the English translation."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, uploaded]
        )

        return response.text.strip()

    except Exception as e:
        print("Error:", str(e))
        return "❌ Error processing the audio: " + str(e)
