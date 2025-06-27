import os
import requests
import subprocess
from google import genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.GenerativeModel("gemini-2.0-flash")

def transcribe_and_translate(media_url):
    # Step 1: Download OGG file from Twilio
    audio_path_ogg = "audio.ogg"
    audio_path_wav = "audio.wav"

    response = requests.get(media_url)
    with open(audio_path_ogg, "wb") as f:
        f.write(response.content)

    # Step 2: Convert OGG to WAV using ffmpeg
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", audio_path_ogg,
        audio_path_wav
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        return "Error: Audio conversion failed. Ensure ffmpeg is installed."

    # Step 3: Upload to Gemini for transcription + translation
    prompt = (
        "Transcribe the following audio.\n"
        "1. Provide the transcription in the original language.\n"
        "2. Provide an English translation."
    )

    upload = client.upload_file(audio_path_wav)
    response = client.generate_content([prompt, upload])

    return response.text.strip()
