import os
import requests
import subprocess
from google import genai

client = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

def transcribe_and_translate(media_url):
    audio_path_ogg = "audio.ogg"
    audio_path_wav = "audio.wav"

    # Step 1: Download audio from Twilio
    response = requests.get(media_url)
    with open(audio_path_ogg, "wb") as f:
        f.write(response.content)

    # Step 2: Convert OGG to WAV
    result = subprocess.run([
        "ffmpeg", "-y", "-i", audio_path_ogg, audio_path_wav
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        return "Error: Failed to convert audio to WAV."

    # Step 3: Use Gemini to transcribe and translate
    prompt = (
        "Transcribe the following audio.\n"
        "1. First, provide the transcription in the original language.\n"
        "2. Then, translate it to English."
    )

    # Upload and send to Gemini
    uploaded = client.upload_file(audio_path_wav)
    response = client.generate_content([prompt, uploaded])

    return response.text.strip()
