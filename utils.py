import os
import requests
import subprocess
from google import genai

# Initializes the Gemini client (auto uses GEMINI_API_KEY from env)
client = genai.Client()

def transcribe_and_translate(media_url):
    audio_path_ogg = "audio.ogg"
    audio_path_wav = "audio.wav"

    # Step 1: Download OGG audio from Twilio
    response = requests.get(media_url)
    with open(audio_path_ogg, "wb") as f:
        f.write(response.content)

    # Step 2: Convert OGG to WAV using FFmpeg
    result = subprocess.run([
        "ffmpeg", "-y", "-i", audio_path_ogg, audio_path_wav
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        return "❌ Error: Failed to convert audio. FFmpeg not working?"

    # Step 3: Upload to Gemini and request transcription + translation
    prompt = (
        "Transcribe the following audio.\n"
        "1. First, show the transcription in the original language.\n"
        "2. Then provide the English translation."
    )

    uploaded = client.files.upload(file=audio_path_wav)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, uploaded]
    )

    return response.text.strip()
