import os
import requests
from google import genai

client = genai.Client()

def transcribe_and_translate(media_url):
    file_name = "audio.mp3"  # Can also be .wav

    try:
        # Download file directly
        response = requests.get(media_url)
        with open(file_name, "wb") as f:
            f.write(response.content)

        # Upload to Gemini
        upload = client.files.upload(file=file_name)

        prompt = (
            "Transcribe and translate this audio file:\n"
            "1. Show the original language transcription.\n"
            "2. Provide the English translation."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, upload]
        )

        return response.text.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"
