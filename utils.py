import os
import requests
import subprocess
from google import genai

client = genai.Client()

def transcribe_and_translate(media_url):
    ogg_file = "audio.ogg"
    wav_file = "audio.wav"

    try:
        # Step 1: Download audio file
        response = requests.get(media_url)
        with open(ogg_file, "wb") as f:
            f.write(response.content)

        # Step 2: Convert OGG to WAV using ffmpeg
        result = subprocess.run([
            "ffmpeg", "-y", "-i", ogg_file, wav_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return "❌ Error: Audio conversion failed. FFmpeg may not be installed."

        # Step 3: Upload to Gemini
        upload = client.files.upload(file=wav_file)
        prompt = (
            "Transcribe and translate this audio file:\n"
            "1. Transcribe in the original language.\n"
            "2. Translate to English."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, upload]
        )

        return response.text.strip()

    except Exception as e:
        print("❌ Exception:", e)
        return "❌ Error processing audio: " + str(e)
